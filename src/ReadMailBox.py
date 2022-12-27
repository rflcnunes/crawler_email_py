import json
import os
import re

import dotenv
import imap_tools

import packages


class ReadMailBox:
    def __init__(self):
        dotenv.load_dotenv()
        self.HOST = os.environ.get('IMAP_GMAIL_HOST')
        self.USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
        self.PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')
        self.QUEUE = os.environ.get('RABBITMQ_DEFAULT_QUEUE')
        self.RABBIT_STATUS = os.environ.get('CRAWLER_RABBIT_ACTIVE')
        self.MAILBOX_READ = input('Enter the mailbox name: ')
        self.PATH_TEMP_ATTACHMENTS = 'attachments/'
        self.CRAWLER_BUCKET = os.environ.get('CRAWLER_BUCKET')

    @staticmethod
    def format_data(message):
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        message = re.sub(cleaner, '', message)
        message = re.sub(r'http\S+', '', message)

        return message

    def read_mailbox(self):
        with imap_tools.MailBox(self.HOST).login(self.USERNAME, self.PASSWORD) as mailbox:
            try:
                mailbox.folder.set(self.MAILBOX_READ)
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
                        'body': self.format_data(msg.text),
                        'html': msg.html,
                        'messageId': msg.uid,
                    }

                    if not msg.to:
                        data['to'] = msg.headers['bcc']

                    if not data['body'] and data['subject']:
                        data['body'] = data['subject']

                    for attachment in msg.attachments:
                        data['attachments'] = {
                            'is_attachment': True,
                            'filename': attachment.filename,
                        }

                    data = json.dumps(data)

                    if self.RABBIT_STATUS != 'True':
                        return False
                    packages.rabbit_mq.Publisher(host=self.HOST, queue=self.QUEUE, message=data, exchange='').publish()

                    if msg.attachments:
                        for attachment in msg.attachments:
                            file_name = attachment.filename
                            file_path = self.PATH_TEMP_ATTACHMENTS + file_name

                            if os.path.isdir(file_path):
                                continue

                            with open(file_path, 'wb') as f:
                                f.write(attachment.payload)

                            # packages.storage_bucket.MinioBucket.upload_file(self.CRAWLER_BUCKET, file_name, file_path)
                            # os.remove(file_path)
