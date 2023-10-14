from smtplib import SMTP_SSL
from email.message import EmailMessage
from dotenv import dotenv_values
from constants.info_message import InfoMessage
import logging
import json
from dao.mongodao import WasteManagementDao
import time

logger = logging.getLogger("log")
config = dotenv_values(".env")


async def send_mail(contacts, mail_add):
    msg = EmailMessage()
    contacts = json.dumps(contacts)

    logger.info(contacts)
    msg["From"] = config["EMAIL_SENDER"]
    msg["Subject"] = "Verification code"
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           {}
        </p>
      </body>
    </html>
    """
    with SMTP_SSL(config["EMAIL_SERVER"], 465) as smtp:
        msg.add_alternative(html.format(contacts), subtype="html")
        smtp.login(config["EMAIL_SENDER"], config["PASSWORD"])
        smtp.send_message(msg, to_addrs=mail_add)
    logger.info(InfoMessage.EMAIL)
    return True


def expire_verification_code(condition, expire):

    dao = WasteManagementDao(config["USER_COLLECTION_NAME"], config["DB_NAME"])
    time.sleep(120)
    dao.db.find_one_and_update(condition, expire)
    pass
