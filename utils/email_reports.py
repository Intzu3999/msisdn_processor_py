import smtplib
import email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
from ..config import EMAIL_USER, EMAIL_PASSWORD, EMAIL_TO, SMTP_SERVER, SMTP_PORT
from .collect_reports import collect_recent_reports
from .email_reports import send_reports
from utils.datetime_utils import date_with_time
import os

def email_reports(file_paths, subject=f"Automated Report - {date_with_time}", body=f"Attached are your latest reports - {date_with_time}"):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for path in file_paths:
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=path.split("/")[-1])
            part["Content-Disposition"] = f'attachment; filename="{path.split("/")[-1]}"'
            msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent successfully with {len(file_paths)} attachment(s).")
    except Exception as e:
        print("❌ Email send failed:", e)

def send_latest_reports():
    reports = collect_recent_reports(result_folder="result")
    if not reports:
        print("⚠️ No new reports found to send.")
        return
    send_reports(
        reports,
        subject="Automated Test Report",
        body="Attached are the latest generated reports."
    )

def send_email():
    sender = os.getenv("EMAIL_USER")
    recipient = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText("Test email from GitHub Actions CI pipeline.")
    msg["Subject"] = "Test Execution Report - DD.MM.YYYY"
    msg["From"] = sender
    msg["To"] = recipient

    # ---- Gmail ----
    smtp_server = "smtp.gmail.com"
    port = 465
    use_ssl = True

    # ---- Outlook/Office365 ----
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
    email_reports()
