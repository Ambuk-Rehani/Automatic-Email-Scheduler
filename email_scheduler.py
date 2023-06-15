import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from jinja2 import Template
import re
from datetime import datetime

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

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_date_time(date, time):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        datetime.strptime(time, '%H:%M')
        return True
    except ValueError:
        return False
    
def get_email_details():
    recipient = input("Recipient's Email Address: ")
    subject = input("Subject: ")
    message = input("Message: ")
    date = input("Date (YYYY-MM-DD): ")
    time = input("Time (HH:MM): ")
    
    return recipient, subject, message, date, time

def main():
    recipient, subject, message, date, time = get_email_details()
    
    
    if not validate_email(recipient):
        print("Invalid email address format. Please enter a valid email address.")
        return
    
    if not validate_date_time(date, time):
        print("Invalid date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).")
        return
    
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