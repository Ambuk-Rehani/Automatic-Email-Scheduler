import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'rehaniambuk@gmail.com'
SMTP_PASSWORD = 'ejxhzapmftcfikgj'

def send_email(sender_email, receiver_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Establish a connection with the SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Start a secure connection
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def main():
    sender_email = 'rehaniambuk@gmail.com'
    receiver_email = 'oneahsan3596@gmail.com'
    subject = 'Hello from the Automated Email Scheduler'
    message = 'This is a test email.'

    send_email(sender_email, receiver_email, subject, message)

if __name__ == '__main__':
    main()