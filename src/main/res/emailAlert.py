from .sharedconstants import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from os.path import join, split


def substitute_vars(string, provider, location, name, size, hash):
    size = str(size)
    loc_type = "Container" if provider == "Azure" else "Bucket"
    return string.replace("{PROVIDER}", provider).replace("{LOCATION}", location).replace("{NAME}", name).replace(
        "{SIZE}", size).replace("{HASH}", hash).replace("{LOCATION_TYPE}", loc_type)


def send_email(provider, location, name, size, hash):
    if not size:
        logger.info("Blank / Non-existent file. Skipping...")
        return
    msg = MIMEMultipart("alternative")
    msg["subject"] = substitute_vars(SUBJECT, provider, location, name, size, hash)
    msg["from"] = formataddr((SENDER_DISP_NAME, SENDER_EMAIL))
    msg["to"] = DEST_EMAIL
    msg["reply-to"] = None

    with open(join(split(__file__)[0], "email.txt"), 'r') as f:
        text = f.read()
        part1 = MIMEText(substitute_vars(text, provider, location, name, size, hash), "text")
        msg.attach(part1)

    with open(join(split(__file__)[0], "email.html"), 'r') as f:
        htmltext = f.read()
        part2 = MIMEText(substitute_vars(htmltext, provider, location, name, size, hash), "html")
        msg.attach(part2)

    context = ssl.create_default_context()
    server = None
    try:
        if PROTOCOL == "TLS":
            port = 587
            server = smtplib.SMTP(SMTP_SERVER, port)
            server.starttls(context=context)
        elif PROTOCOL == "SSL":
            port = 465
            server = smtplib.SMTP_SSL(SMTP_SERVER, port, context=context)
        # I doubt it but if someone wants to have the option of choosing no TLS/SSL,
        # you need an elif here and to edit the tuple in sharedconstants.py line 30
        else:
            raise RuntimeError("Invalid protocol.")
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)
        print(msg.as_string())
    finally:
        if server is not None:
            server.quit()
