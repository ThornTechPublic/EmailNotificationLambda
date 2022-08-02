from .sharedconstants import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from os.path import join, split
import re


def substitute_vars(string, provider, location, filepath, size, md5hash, **kwargs):
    loc_type = "Container" if provider == "Azure" else "Bucket"
    match_obj = re.match(r"users/(.+?)/.+", filepath)
    user = "None" if match_obj is None else match_obj.group(1)
    directory, filename = split(filepath)
    subs_dict = {"{PROVIDER}": provider, "{LOCATION}": location, "{FILEPATH}": filepath, "{SIZE}": size, "{HASH}": md5hash,
                 "{LOCATION_TYPE}": loc_type, "{USER}": user, "{DIRECTORY}": directory, "{FILENAME}": filename}
    subs_dict.update({k.upper().join("{}"): v for k, v in kwargs.items()})
    for k, v in subs_dict.items():
        string = string.replace(k, str(v))
    return string


def send_email(provider, location, filepath, size, md5hash, **kwargs):
    if not size:
        logger.info("Blank / Non-existent file. Skipping...")
        return
    msg = MIMEMultipart("alternative")
    msg["subject"] = substitute_vars(SUBJECT, provider, location, filepath, size, md5hash, **kwargs)
    msg["from"] = formataddr((SENDER_DISP_NAME, SENDER_EMAIL))
    msg["to"] = DEST_EMAIL
    msg["reply-to"] = None

    with open(join(split(__file__)[0], "email.txt"), 'r') as f:
        text = f.read()
        part1 = MIMEText(substitute_vars(text, provider, location, filepath, size, md5hash, **kwargs), "text")
        msg.attach(part1)

    with open(join(split(__file__)[0], "email.html"), 'r') as f:
        htmltext = f.read()
        part2 = MIMEText(substitute_vars(htmltext, provider, location, filepath, size, md5hash, **kwargs), "html")
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
        logger.info(msg.as_string())
        logger.info("Message sent!")
    except Exception:
        logger.error("Message not sent!")
        raise
    finally:
        if server is not None:
            logger.info("Quitting server")
            server.quit()
