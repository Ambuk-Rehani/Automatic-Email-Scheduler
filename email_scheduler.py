from config_handler import load_config
from db_handler import connect_db, check_create_table
from email_handler import send_email
from input_handler import get_email_details, validate_email, validate_date_time
from jinja2 import Template
import logging

def main():
    # Load configuration and connect to the database
    config = load_config()
    conn = connect_db()
    
    # SMTP server configuration
    smtp_server = config['SMTP']['server']
    smtp_port = config['SMTP']['port']
    smtp_username = config['SMTP']['username']
    smtp_password = config['SMTP']['password']

    check_create_table(conn)
    
    # Get email details from the user
    recipient, subject, message, date, time = get_email_details()

    if not validate_email(recipient):
        print("Invalid email address format. Please enter a valid email address.")
        return
    
    if not validate_date_time(date, time):
        print("Invalid date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).")
        return

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO scheduled_emails (recipient, subject, message, date, time, status)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (recipient, subject, message, date, time, "scheduled"))
        conn.commit()
        
    print("Email scheduled successfully.")

if __name__ == '__main__':
    logging.basicConfig(filename='email_scheduler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
