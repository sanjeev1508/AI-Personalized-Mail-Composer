import imaplib
import email
import json
import os
import re

N_EMAILS = 100

def clean_text(text):
    text = re.sub(r'\s+', ' ', text.strip().replace("\r", "").replace("\n", " "))
    return text[:1000]  # Trim overly long content

def is_forwarded(subject):
    subject_lower = subject.lower()
    return subject_lower.startswith("fwd:") or subject_lower.startswith("fw:")

def is_junk_body(body):
    return len(body.strip()) < 20 or 'pdf' in body.lower() or 'content-type' in body.lower()

def fetch_sent_emails(user_email, app_password, output_path):
    print("🔄 Connecting to Gmail IMAP...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user_email, app_password)
    mail.select('"[Gmail]/Sent Mail"')

    result, data = mail.search(None, "ALL")
    mail_ids = data[0].split()
    last_ids = mail_ids[-N_EMAILS:]

    emails = []
    skipped = 0

    for i in last_ids:
        result, data = mail.fetch(i, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg.get("Subject", "(No Subject)").strip()
        if is_forwarded(subject):
            skipped += 1
            continue

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
            except:
                continue

        if is_junk_body(body):
            skipped += 1
            continue

        emails.append({
            "subject": clean_text(subject),
            "body": clean_text(body)
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(emails)} clean sent mails to {output_path}")
    print(f"⚠️ Skipped {skipped} forwarded or invalid entries.")

    return emails  # optional: return for use in app

# Example usage:
if __name__ == "__main__":
    email_input = input("Enter your Gmail address: ").strip()
    app_password_input = input("Enter your App Password: ").strip()
    output_file = r"C:\sanjeev\custom_mail_bot\data\sent_emails.json"
    fetch_sent_emails(email_input, app_password_input, output_file)
