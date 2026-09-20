"""
Bulk Email Sender (Gmail SMTP)
------------------------------
Sends a SEPARATE email (same subject/body/attachment) to every recipient
listed in a CSV file, one email per recipient (not one email with everyone
in CC/BCC).

SETUP
-----
1. You need a Gmail "App Password" (NOT your normal Gmail password):
   - Turn on 2-Step Verification on your Google account:
     https://myaccount.google.com/security
   - Generate an App Password here:
     https://myaccount.google.com/apppasswords
   - Use that 16-character password below (GMAIL_APP_PASSWORD).

2. Install dependencies (only standard library is used, so nothing to install).

3. Create a CSV file named `recipients.csv` with one column `email`:

       email
       person1@example.com
       person2@example.com
       person3@example.com

4. Edit the CONFIG section below (sender email, app password, subject,
   body, attachment path, path to recipients.csv).

5. Run:
       python send_bulk_emails.py

The script sends one-by-one with a short delay between sends to avoid
tripping Gmail's spam/rate limits, and prints a success/failure log for
each recipient.
"""

import smtplib
import ssl
import csv
import time
import os
import sys
from email.message import EmailMessage

# ============ CONFIG — EDIT THESE ============

GMAIL_ADDRESS = "abc@gmail.com"          # Your Gmail address
GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"      # 16-char App Password (not your login password)

SUBJECT = "Application for Software Developer / Associate Software Developer Position - Harsh Barbhai"
BODY = """
"""# """" write your subject body here   """"

ATTACHMENT_PATH = "enter your file path here"         # Path to the file you want to attach (set to "" for no attachment)

RECIPIENTS_CSV = "emails.csv"               # CSV file with a column named "email"

DELAY_BETWEEN_EMAILS_SECONDS = 2             # Be polite to Gmail's servers; increase if you send many emails

# ===============================================


def load_recipients(csv_path):
    if not os.path.exists(csv_path):
        print(f"ERROR: Recipients file not found: {csv_path}")
        sys.exit(1)

    emails = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "email" not in (reader.fieldnames or []):
            print('ERROR: CSV must have a column header named "email"')
            sys.exit(1)
        for row in reader:
            addr = row["email"].strip()
            if addr:
                emails.append(addr)
    return emails


def build_message(to_addr, from_addr, subject, body, attachment_path):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment_path:
        if not os.path.exists(attachment_path):
            raise FileNotFoundError(f"Attachment not found: {attachment_path}")
        with open(attachment_path, "rb") as f:
            file_data = f.read()
        file_name = os.path.basename(attachment_path)
        # Guess a generic type; Gmail handles octet-stream fine for any file
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name,
        )
    return msg


def send_all():
    recipients = load_recipients(RECIPIENTS_CSV)
    if not recipients:
        print("No recipients found in CSV. Exiting.")
        return

    print(f"Loaded {len(recipients)} recipient(s). Starting send...\n")

    context = ssl.create_default_context()
    sent, failed = [], []

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

        for i, to_addr in enumerate(recipients, start=1):
            try:
                msg = build_message(to_addr, GMAIL_ADDRESS, SUBJECT, BODY, ATTACHMENT_PATH)
                server.send_message(msg)
                print(f"[{i}/{len(recipients)}] Sent to {to_addr}")
                sent.append(to_addr)
            except Exception as e:
                print(f"[{i}/{len(recipients)}] FAILED to send to {to_addr}: {e}")
                failed.append((to_addr, str(e)))

            # Delay between sends (skip delay after the last email)
            if i < len(recipients):
                time.sleep(DELAY_BETWEEN_EMAILS_SECONDS)

    print("\n---- Summary ----")
    print(f"Sent:   {len(sent)}")
    print(f"Failed: {len(failed)}")
    if failed:
        for addr, err in failed:
            print(f"  - {addr}: {err}")


if __name__ == "__main__":
    send_all()
