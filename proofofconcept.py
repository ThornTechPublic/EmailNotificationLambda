import os
import sys

try:
    email_addr = sys.argv[1]
except IndexError:
    email_addr = input("What email address are you using? ")

os.environ["SENDER_EMAIL"] = email_addr
os.environ["SENDER_DISP_NAME"] = "EAA Sys"
os.environ["DEST_EMAIL"] = email_addr
os.environ["SMTP_SERVER"] = "smtp.gmail.com"

with open("apppass") as f:
    os.environ["PASSWORD"] = f.readline().strip()
import src.main.res.emailAlert as EA
EA.send_email("Test Provider", "Empty Bucket", "No One", 0, "hashbrown")
