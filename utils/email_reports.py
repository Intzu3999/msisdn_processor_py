import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.datetime_utils import date_with_time
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
RESULT_FOLDER = "result"
VALID_EXTENSIONS = (".xlsx", ".csv", ".html")

def email_reports(
    file_paths,
    subject=None,
    body=None,
):

    if not file_paths:
        print("⚠️ No files provided to email.")
        return

    # Default subject/body with current timestamp
    current_time = date_with_time()
    subject = subject or f"CI/CD Report - {current_time}"
    body = body or f"Attached are your latest reports - {current_time}"

    # Compose email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach each file
    for path in file_paths:
        try:
            with open(path, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(path))
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
                msg.attach(part)
        except Exception as e:
            print(f"⚠️ Could not attach {path}: {e}")

    # Send email
    try:
        if SMTP_PORT == 465:
            # Gmail SSL port
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
        else:
            # TLS (e.g., Outlook/Office365)
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)

        print(f"✅ Email sent successfully to {EMAIL_TO} with {len(file_paths)} file(s).")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# def collect_recent_reports(result_folder="../result", hours=1):
#     collected = []
#     cutoff = datetime.now() - timedelta(hours=hours)

#     if not os.path.exists(result_folder):
#         print(f"⚠️ Folder '{result_folder}' does not exist.")
#         return collected

#     for fname in os.listdir(result_folder):
#         if fname.endswith(VALID_EXTENSIONS):
#             full_path = os.path.join(result_folder, fname)
#             mtime = datetime.fromtimestamp(os.path.getmtime(full_path))
#             if mtime > cutoff:
#                 collected.append(full_path)
#     return collected

# def email_reports(file_paths, subject=f"CI/CD Report - {date_with_time}", body=f"Attached are your latest reports - {date_with_time}"):
#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_USER
#     msg["To"] = EMAIL_TO
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain"))

#     for path in file_paths:
#         try:
#             with open(path, "rb") as f:
#                 part = MIMEApplication(f.read(), Name=os.path.basename(path))
#                 part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
#                 msg.attach(part)
#         except Exception as e:
#             print(f"⚠️ Could not attach {path}: {e}")

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(EMAIL_USER, EMAIL_PASSWORD)
#             server.send_message(msg)
#         print(f"✅ Email sent successfully to {EMAIL_TO} with {len(file_paths)} file(s).")
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}")

# def send_latest_reports(result_folder="results"):
#     reports = collect_recent_reports(result_folder=result_folder)
#     if not reports:
#         print("⚠️ No new reports found to send.")
#         return
#     email_reports(reports)

# def send_email():
#     sender = os.getenv("EMAIL_USER")
#     recipient = os.getenv("EMAIL_TO")
#     password = os.getenv("EMAIL_PASSWORD")

#     msg = MIMEText("Test email from GitHub Actions CI pipeline.")
#     msg["Subject"] = "Test Execution Report - DD.MM.YYYY"
#     msg["From"] = sender
#     msg["To"] = recipient

#     # ---- Gmail ----
#     smtp_server = "smtp.gmail.com"
#     port = 465
#     use_ssl = True

#     # ---- Outlook/Office365 ----
#     # smtp_server = "smtp.office365.com"
#     # port = 587
#     # use_ssl = False

#     try:
#         if use_ssl:
#             with smtplib.SMTP_SSL(smtp_server, port) as server:
#                 server.login(sender, password)
#                 server.send_message(msg)
#         else:
#             with smtplib.SMTP(smtp_server, port) as server:
#                 server.starttls()
#                 server.login(sender, password)
#                 server.send_message(msg)
#         print("✅ Email sent:", recipient)
#     except Exception as e:
#         print("❌ Failed to send email:", e)

if __name__ == "__main__":
    email_reports()
