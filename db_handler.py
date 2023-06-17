import psycopg2

def connect_db():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="email_scheduler",
        user="postgres",
        password="ambuk"
    )
    return conn

def check_create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'scheduled_emails'
            );
        """)
        table_exists = cursor.fetchone()[0]

    # Create the scheduled_emails table if it doesn't exist
    if not table_exists:
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
            conn.commit()
