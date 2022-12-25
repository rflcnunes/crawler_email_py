import json
import os

import dotenv
from imap_tools import MailBox

import bucket.send_to_minio_bucket
import rabbitmq.publish

dotenv.load_dotenv()
HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')
QUEUE = os.environ.get('RABBITMQ_DEFAULT_QUEUE')
RABBIT_STATUS = os.environ.get('CRAWLER_RABBIT_ACTIVE')
MAILBOX_READ = input('Enter the mailbox name: ')
PATH_TEMP_ATTACHMENTS = 'attachments/'
CRAWLER_BUCKET = os.environ.get('CRAWLER_BUCKET')


def read_mailbox():
    try:
        with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
            try:
                mailbox.folder.set(MAILBOX_READ)
            except Exception as exception:
                print("Not found mailbox: ", exception)

            status = mailbox.folder.status()
            print(f'Total messages: {status["MESSAGES"]}')

            for msg in mailbox.fetch(reverse=True, mark_seen=False):
                if not msg.headers:
                    raise Exception("Header is empty")
                else:
                    data = {
                        'from': msg.from_,
                        'to': msg.to,
                        'headers': msg.headers,
                        'subject': msg.subject,
                        'body': msg.text,
                        'html': msg.html,
                        'messageId': msg.uid,
                    }

                    if not data['body'] and data['subject']:
                        data['body'] = data['subject']

                    for attachment in msg.attachments:
                        data['attachments'] = {
                            'is_attachment': True,
                            'filename': attachment.filename,
                        }

                    data = json.dumps(data)

                    if RABBIT_STATUS != 'True':
                        return False

                    rabbitmq.publish.publish(QUEUE, data)

                    if msg.attachments:
                        for attachment in msg.attachments:
                            file_name = attachment.filename
                            file_path = PATH_TEMP_ATTACHMENTS + file_name

                            if os.path.isdir(file_path):
                                continue

                            with open(file_path, 'wb') as f:
                                f.write(attachment.payload)

                            bucket.send_to_minio_bucket.upload_file(CRAWLER_BUCKET, file_name, file_path)
                            os.remove(file_path)

    except Exception as e:
        print(f" [ ] Error: {e} - {type(e)} - {e.args} - {e.__traceback__}")


read_mailbox()
