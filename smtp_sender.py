import smtplib
from email.mime.text import MIMEText

def send_email_smtp(to_email, subject, body):
    sender_email = "your-mail@gmail.com"
    app_password = "App-password"'''   # How to get App Password:
                                                1. Go to Google Account
                                                2. Search for "App Passwords"
                                                3. Generate a name
                                                4. Copy the password and paste it here'''  

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
