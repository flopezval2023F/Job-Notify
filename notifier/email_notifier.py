import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env for email credentials
load_dotenv()

# Get email credentials from environment variables
EMAIL_ADDRESS = os.getenv("GMAIL_USER")
EMAIL_PASSWORD = os.getenv("GMAIL_PASS")

# Function to send an email with the given subject and body
def send_email_notification(to_email, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    try:
        # Connect to Gmail SMTP server using SSL 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login with app password
            smtp.send_message(msg)  # Send the email
            print(f"[EMAIL] Sent to {to_email}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")  # Print error if sending fails
