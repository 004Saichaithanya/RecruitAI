import smtplib
from email.message import EmailMessage

def send_emails(emails, candidates):
    sender = "youremail@example.com"
    password = "yourpassword"  # or use environment variable

    msg_body = "You are shortlisted for an interview!\n\nShortlisted Candidates:\n"
    for c in candidates:
        msg_body += f"- {c['name']} (Score: {c['score']:.2f})\n"

    for email in emails:
        msg = EmailMessage()
        msg.set_content(msg_body)
        msg["Subject"] = "Interview Shortlist Notification"
        msg["From"] = sender
        msg["To"] = email.strip()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
