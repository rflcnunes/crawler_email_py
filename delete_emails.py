import csv
import logging
import os
from datetime import date

from dotenv import load_dotenv
from imap_tools import MailBox

load_dotenv()

logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG
                    )

HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')

MAILBOX_FROM = input('From mailbox: ')
MAILBOX_WORD_FILTER = input('Mailbox word filter: ')

ACTUAL_DATE = date.today().strftime("%d-%m-%Y")
LOG_FILE_ACTIONS = f'logs/actions_logging_{ACTUAL_DATE}.csv'
LOG_FILE_BALANCE = f'logs/balance_logging_{ACTUAL_DATE}.csv'

hasLogActions = os.path.isfile(LOG_FILE_ACTIONS)
hasLogBalance = os.path.isfile(LOG_FILE_BALANCE)


def save_log_actions(email, context, id):
    try:
        with open(LOG_FILE_ACTIONS, 'a', newline='') as csv_file:
            fieldnames = ['email', 'context', 'id']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not hasLogActions:
                writer.writeheader()

            writer.writerow({
                'email': email,
                'context': context,
                'id': id
            })

    except Exception as e:
        logging.error(f"Error: {e}, {e.args}")
        return False


def save_log_balance(no_match, deleted, verified):
    try:
        with open(LOG_FILE_BALANCE, 'a', newline='') as csv_file:
            fieldnames = ['no_match', 'deleted', 'verified']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not hasLogBalance:
                writer.writeheader()

            writer.writerow({
                'no_match': no_match,
                'deleted': deleted,
                'verified': verified
            })

    except Exception as e:
        logging.error(f"Error: {e}, {e.args}")
        return False


def delete_emails():
    try:
        with MailBox(HOST).login(USERNAME, PASSWORD, initial_folder=MAILBOX_FROM) as mailbox:
            emails = mailbox.fetch(mark_seen=False)
            total_emails_deleted = 0
            total_emails_not_match = 0
            total_verified_emails = 0

            for email in emails:
                if MAILBOX_WORD_FILTER in email.text:
                    print(f"Deleting email with uid {email.uid}")

                    mailbox.delete(email.uid)
                    mailbox.expunge()
                    total_emails_deleted += 1

                    save_log_actions(email.text, 'deleted', email.uid)

                else:
                    print(f"Email with uid {email.uid} does not match")
                    total_emails_not_match += 1

                total_verified_emails += 1

            print("------------------------")
            print(f"Total emails with not match: {total_emails_not_match}")
            print(f"Total emails deleted: {total_emails_deleted}")
            print(f"Total verified emails: {total_verified_emails}")
            print("------------------------")

            save_log_balance(total_emails_not_match, total_emails_deleted, total_verified_emails)

    except Exception as e:
        logging.error(f"Error: {e}, {e.args}")
        return False
