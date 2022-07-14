import logging
import os

# Logger
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('LOG_LEVEL', default='INFO')))
logger.info('Loading function')

# Global variables
SENDER_DISP_NAME = os.getenv("SENDER_DISP_NAME")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
if not SENDER_EMAIL:
    raise EnvironmentError(f"SENDER_EMAIL is required!")
DEST_DISP_NAME = os.getenv("DEST_DISP_NAME")
DEST_EMAIL = os.getenv("DEST_EMAIL")
if not DEST_EMAIL:
    raise EnvironmentError(f"DEST_EMAIL is required!")
PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise EnvironmentError(f"PASSWORD is required!")
SMTP_SERVER = os.getenv("SMTP_SERVER", f"smtp.{SENDER_EMAIL.replace('@', '.').split('.')[-2]}.com")
SUBJECT = os.getenv("SUBJECT", "A file was uploaded to {LOCATION}!") #Intentionally not an f-string!
PROTOCOL = os.getenv("PROTOCOL", "TLS").upper()
if PROTOCOL not in ("TLS", "SSL"):
    raise EnvironmentError(f"Protocol {PROTOCOL} not recognized! Only valid options are TLS and SSL.")

trim_path_to_filename = os.path.basename
trim_path_to_directory = os.path.dirname
