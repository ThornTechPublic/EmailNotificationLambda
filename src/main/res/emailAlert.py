from .sharedconstants import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


def substitute_vars(string, provider, location, name, size, hash):
    size = str(size)
    return string.replace("{PROVIDER}", provider).replace("{LOCATION}", location).replace("{NAME}", name).replace(
        "{SIZE}", size).replace("{HASH}", hash)


def send_email(provider, location, name, size, hash):
    msg = MIMEMultipart("alternative")
    msg["subject"] = substitute_vars(SUBJECT, provider, location, name, size, hash)
    msg["from"] = formataddr((SENDER_DISP_NAME, SENDER_EMAIL))
    msg["reply-to"] = None

    loc_type = "Container" if provider == "Azure" else "Bucket"

    part1 = MIMEText(f"""This email has been sent because a file was uploaded to cloud storage.
Cloud Provider: {provider}
{loc_type}: {location}
Filepath: {name}
Size: {size}
Hash: {hash}""", "text")

    with open("../res/email.html") as f:
        htmltext = f.read()
    part2 = MIMEText(substitute_vars(htmltext, provider, location, name, size, hash).replace("{LOC_TYPE}", loc_type), "html")
    msg.attach(part1)
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
        else:
            raise RuntimeError("Invalid protocol.")
        server.login(SENDER_EMAIL, PASSWORD)
        msg["to"] = DEST_EMAIL
        server.send_message(msg)
        print(msg.as_string())
    finally:
        if server is not None:
            server.quit()
