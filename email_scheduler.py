import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from jinja2 import Template

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')


with open('email_template.html', 'r') as file:
    email_template = Template(file.read())

# SMTP server configuration
smtp_server = config['SMTP']['server']
smtp_port = config['SMTP']['port']
smtp_username = config['SMTP']['username']
smtp_password = config['SMTP']['password']

def send_email(recipient, subject, message):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    # Establish a connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Start a secure connection
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        
    print("Email sent successfully")
    
def get_email_details():
    recipient = input("Recipient's Email Address: ")
    subject = input("Subject: ")
    message = input("Message: ")
    
    return recipient, subject, message

def main():
    recipient, subject, message = get_email_details()
    
    # Replace placeholders in the email template with actual values
    email_body = email_template.render(
        recipient=recipient,
        subject=subject,
        message=message
    )
    
    # Send the email
    send_email(recipient, subject, email_body)

if __name__ == '__main__':
    main()