import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_email(smtp_server, smtp_port, smtp_username, smtp_password, recipient, subject, message):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start a secure connection
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        logging.info('f"Email sent to {recipient}"')
        
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {e}")
        return False

    return True
