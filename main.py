import json
import os

import dotenv
from imap_tools import MailBox

import rabbitmq.publish

dotenv.load_dotenv()
HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')
QUEUE = os.environ.get('RABBITMQ_DEFAULT_QUEUE')
RABBIT_STATUS = os.environ.get('CRAWLER_RABBIT_ACTIVE')


def read_mailbox():
    try:
        with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
            mailbox.folder.set('crawler_test')
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

    except Exception as e:
        print(e)
