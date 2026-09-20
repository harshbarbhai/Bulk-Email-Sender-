# Bulk-Email-Sender-
Python-based application that automates sending personalized emails to multiple recipients using SMTP.
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
