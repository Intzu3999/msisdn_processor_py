import smtplib
from email.mime.text import MIMEText
import os

def send_email():
    sender = os.getenv("EMAIL_USER")
    recipient = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText("Test email from GitHub Actions CI pipeline.")
    msg["Subject"] = "Test Execution Report - DD.MM.YYYY"
    msg["From"] = sender
    msg["To"] = recipient

    # mail server to use
    # ---- For Gmail ----
    smtp_server = "smtp.gmail.com"
    port = 465
    use_ssl = True

    # ---- For Outlook/Office365 ----
    # smtp_server = "smtp.office365.com"
    # port = 587
    # use_ssl = False

    try:
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_server, port) as server:
                server.login(sender, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
        print("✅ Email sent:", recipient)
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    send_email()
