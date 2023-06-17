import re
from datetime import datetime

def get_email_details():
    recipient = input("Recipient's Email Address: ")
    subject = input("Subject: ")
    message = input("Message: ")
    date = input("Date (YYYY-MM-DD): ")
    time = input("Time (HH:MM): ")
    
    return recipient, subject, message, date, time

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
