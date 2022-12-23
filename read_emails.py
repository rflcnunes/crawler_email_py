import os

import dotenv
from imap_tools import MailBox

dotenv.load_dotenv()
HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')
MAILBOX = input('Enter the mailbox name: ')


def read_email():
    with MailBox(HOST).login(USERNAME, PASSWORD) as mailbox:
        status = mailbox.folder.status(MAILBOX)

        print(f'Total messages: {status["MESSAGES"]}')
