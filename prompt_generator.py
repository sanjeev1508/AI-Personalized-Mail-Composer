def build_prompt(recipient, purpose, full_name, email_samples, signature):
    sample_text = ""
    for i, email in enumerate(email_samples, 1):
        subject = email.get("subject", "(No Subject)").strip()
        body = email.get("body", "").strip()
        sample_text += f"--- Email {i} ---\nSubject: {subject}\nBody:\n{body}\n\n"

    return f"""
You are a helpful assistant trained to write emails that mimic the user's past writing style.

Below are some sample emails written by the user:
{sample_text}

Now, using a similar tone, format, and voice, write a new email.

### New Email Instructions:
- **Recipient Name**: {recipient}
- **Purpose**: {purpose}
- **Signature Name**: {full_name}
- **Preferred Signature Style**: {signature}

### Email Requirements:
- Start with a greeting that includes the recipient’s name (e.g., “Hi {recipient},” or “Dear {recipient},”)
- Use a subject line that reflects the purpose
- Include a clear body with appropriate tone
- End with a polite closing and the user’s signature

Return only the email content. No extra notes or commentary.
"""
