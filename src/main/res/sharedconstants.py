import logging
import os

SMTP_SERVER_DICT = {"aol": "smtp.aol.com", "att": "smtp.mail.att.net", "comcast": "smtp.comcast.net",
                    "icloud": "smtp.mail.me.com", "gmail": "smtp.gmail.com", "outlook": "stmp-mail.outlook.com",
                    "yahoo": "smtp.mail.yahoo.com"}

# Logger
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('LOG_LEVEL', default='INFO')))
logger.info('Loading function')

# Global variables
SENDER_DISP_NAME = os.getenv("SENDER_DISP_NAME")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
if not SENDER_EMAIL:
    raise EnvironmentError(f"SENDER_EMAIL is required!")
DEST_EMAIL = os.getenv("DEST_EMAIL")
if not DEST_EMAIL:
    raise EnvironmentError(f"DEST_EMAIL is required!")
PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise EnvironmentError(f"PASSWORD is required!")
SMTP_SERVER = os.getenv("SMTP_SERVER")
if not SMTP_SERVER:
    domain = SENDER_EMAIL.replace('@', '.').split('.')[-2:]
    SMTP_SERVER = SMTP_SERVER_DICT.get(domain[0].lower(), f"smtp.{domain[0]}.{domain[1]}")
SUBJECT = os.getenv("SUBJECT", "A file was uploaded to {LOCATION}!") #Intentionally not an f-string!
PROTOCOL = os.getenv("PROTOCOL", "TLS").upper()
if PROTOCOL not in ("TLS", "SSL"):
    raise EnvironmentError(f"Protocol {PROTOCOL} not recognized! Only valid options are TLS and SSL.")

trim_path_to_filename = os.path.basename
trim_path_to_directory = os.path.dirname
