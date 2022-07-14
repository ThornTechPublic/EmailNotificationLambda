from .sharedconstants import *
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address, Group, AddressHeader


def substitute_vars(string, provider, location, name, size, hash):
    size = str(size)
    return string.replace("{PROVIDER}", provider).replace("{LOCATION}", location).replace("{NAME}", name).replace(
        "{SIZE}", size).replace("{HASH}", hash)


def send_email(provider, location, name, size, hash):
    msg = MIMEMultipart("alternative")
    msg["subject"] = substitute_vars(SUBJECT, provider, location, name, size, hash)
    msg["from"] = Address(SENDER_DISP_NAME, SENDER_EMAIL) if SENDER_DISP_NAME else SENDER_EMAIL
    #WIP! msg["to"] = AddressHeader(Group("Test Group", ["chris.gick@thorntech.com", "joshbrown@thorntech.com"]))
    msg["to"] = Address(DEST_DISP_NAME, DEST_EMAIL) if DEST_DISP_NAME else DEST_EMAIL
    msg["reply-to"] = None

    loc_type = "Container" if provider == "Azure" else "Bucket"
    part1 = MIMEText(f"""This email has been sent because a file was uploaded to cloud storage.
Cloud Provider: {provider}
{loc_type}: {location}
Filepath: {name}
Size: {size}
Hash: {hash}""", "text")
    part2 = MIMEText(substitute_vars("""\
<html>
    <head>
        <style>
            header{
                text-alignment: center;
                margin: auto;
                font-size: 24px;
            }
            ul{
                color: blue;
            }
            footer{
                color: gray;
            }
        </style>
    </head>
    <body>
        <header>A file was uploaded!</header>
        <section>
            This email has been sent because a file was uploaded to cloud storage.
            <ul>
                <li>Cloud Provider: {PROVIDER}</li>
                <li>{LOC_TYPE}: {LOCATION}</li>
                <li>Filepath: {NAME}</li>
                <li>Size: {SIZE}</li>
                <li>Hash: {HASH}</li>
            </ul>
        </section>
        <footer>This email was auto-generated, please do not reply.</footer>
    </body>
</html>
""", provider, location, name, size, hash).replace("LOC_TYPE", loc_type), "html")
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
        server.send_message(msg)
    finally:
        if server is not None:
            server.quit()
