import logging
import os
import smtplib

import dotenv

dotenv.load_dotenv()
logging.basicConfig(filename='app.log',
                    filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

HOST = os.environ.get('IMAP_GMAIL_HOST')
USERNAME = os.environ.get('IMAP_GMAIL_EMAIL')
PASSWORD = os.environ.get('IMAP_GMAIL_PASSWORD')


def send_email(email, subject, message):
    try:
        from_email = USERNAME
        from_password = PASSWORD

        to_email = email
        subject = subject
        message = message

        msg = "Subject: %s\n\n%s" % (subject, message)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg)
        server.quit()

        return True

    except Exception as e:
        logging.error(f"Error: {e}, {e.args}")
        return False
