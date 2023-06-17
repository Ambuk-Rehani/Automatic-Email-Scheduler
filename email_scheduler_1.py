import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
from jinja2 import Template
import re
from datetime import datetime
import logging
import psycopg2



# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="email_scheduler",
    user="postgres",
    password="ambuk"
)


# Check if the scheduled_emails table already exists
with conn.cursor() as cursor:
    cursor.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'scheduled_emails'
        );
    """)
    table_exists = cursor.fetchone()[0]

# Create the scheduled_emails table
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE scheduled_emails (
            id SERIAL PRIMARY KEY,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            status TEXT NOT NULL
        );
    """)
    

with conn.cursor() as cursor:
    # Insert a new scheduled email
    cursor.execute("""
        INSERT INTO scheduled_emails (recipient, subject, message, date, time, status)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("example@example.com", "Test Subject", "Test Message", "2023-06-07", "10:00:00", "scheduled"))

    # Commit the transaction
    conn.commit()


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
    
    try:
    # Establish a connection with the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start a secure connection
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        logging.info('f"Email sent to {recipient}"')
        
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {e}")
        return False
        
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

def schedule_email(recipient, subject, message, date, time):
    email = {
        'recipient': recipient,
        'subject': subject,
        'message': message,
        'date': date,
        'time': time
    }
    scheduled_emails.append(email)
    
def retrieve_scheduled_emails():
    # Implement logic to retrieve scheduled emails from storage (e.g., database)
    # and populate the scheduled_emails list
    # Here, we'll simulate retrieving from storage by adding a sample email directly
    scheduled_emails.append({
        'recipient': 'example@example.com',
        'subject': 'Sample Subject',
        'message': 'This is a sample message',
        'date': '2023-06-08',
        'time': '09:00',
        'status': 'scheduled'
    })
    
def send_scheduled_emails():
    current_datetime = datetime.now()
    for email in scheduled_emails:
        email_date = datetime.strptime(email['date'], '%Y-%m-%d')
        email_time = datetime.strptime(email['time'], '%H:%M')

        if email_date <= current_datetime.date() and email_time.time() <= current_datetime.time() and email['status'] == 'scheduled':
            success = send_email(email['recipient'], email['subject'], email['message'])
            if success:
                email['status'] = 'sent'

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
    
    schedule_email(recipient, subject, email_body, date, time)

    print("Email scheduled successfully.")
    
    # Send the email
    send_email(recipient, subject, email_body)

if __name__ == '__main__':
    scheduled_emails = []
    logging.basicConfig(filename='email_scheduler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()