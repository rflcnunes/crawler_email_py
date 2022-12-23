import logging
import os

import dotenv
from imap_tools import MailBox

dotenv.load_dotenv()
logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')

MAILBOX_FROM = input('From mailbox: ')
MAILBOX_TO = input('To mailbox: ')


def move_emails():
    try:
        with MailBox(HOST).login(USERNAME, PASSWORD, initial_folder=MAILBOX_FROM) as mailbox:
            moved = ()
            for uid in mailbox.uids():
                print(f'Moving email {uid} from {MAILBOX_FROM} to {MAILBOX_TO}')
                mailbox.move(uid, MAILBOX_TO)
                print(f'Moved message with ID {uid} to {MAILBOX_TO}')
                moved += (uid,)

            print(f'Moved {len(moved)} messages from {MAILBOX_FROM} to {MAILBOX_TO}')

    except Exception as e:
        logging.error(f"Error: {e}, {e.args}")
        return False
