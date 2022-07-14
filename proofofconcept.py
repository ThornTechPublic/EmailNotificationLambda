import os


os.environ["SENDER_EMAIL"] = "joshbrown@thorntechnologies.com"
os.environ["DEST_EMAIL"] = "joshbrown@thorntechnologies.com"
os.environ["SMTP_SERVER"] = "smtp.gmail.com"

with open("apppass") as f:
    os.environ["PASSWORD"] = f.readline().strip()
import src.main.res.emailAlert as EA
EA.send_email("Test Provider", "Empty Bucket", "No One", 0, "hashbrown")