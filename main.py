import os

import dotenv
from imap_tools import MailBox

dotenv.load_dotenv()
HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')


def read_mailbox():
    try:
        with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
            mailbox.folder.set('INBOX')
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

    except Exception as e:
        print(e)
