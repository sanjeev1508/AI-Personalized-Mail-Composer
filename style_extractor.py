import json
import re

def load_email_samples(file_path="data/sent_emails.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        emails = json.load(f)

    # Ensure valid format: list of dicts with 'subject' and 'body'
    valid_emails = []
    for email in emails:
        if isinstance(email, dict) and "subject" in email and "body" in email:
            valid_emails.append({
                "subject": clean_text(email["subject"]),
                "body": clean_text(email["body"])
            })

    return valid_emails

def clean_text(text):
    """Cleans line breaks and excessive spacing"""
    return ' '.join(text.replace("\r", "").replace("\n", "\n").split())

def extract_closing_lines(email_body):
    """Extracts closing phrases like 'Thanks', 'Best regards', etc."""
    lines = email_body.strip().split("\n")
    closings = []
    for line in reversed(lines[-5:]):  # look only at the last 5 lines
        line = line.strip()
        if re.search(r"(regards|thank|sincerely|best|cheers)", line, re.IGNORECASE):
            closings.append(line)
    return closings

def get_style_context(emails):
    """
    Extracts the most common signature from past email samples
    and returns both the emails and the deduced signature.
    """
    closings = []

    for email in emails:
        body = email.get("body", "")
        closings += extract_closing_lines(body)

    # Most frequent closing line or a default fallback
    signature = max(set(closings), key=closings.count) if closings else "Best regards,\nYour Name"

    return {
        "emails": emails,
        "signature": signature
    }
