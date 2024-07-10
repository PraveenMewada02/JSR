import pandas as pd
from sqlalchemy import create_engine, exc
from sqlalchemy.dialects import postgresql  # Ensure PostgreSQL dialect is explicitly imported
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
#import schedule
import time

# Database URL
database_url = "postgresql://default:uWiPqh7zO4SQ@ep-square-wood-a15wl9fx.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'pravinmewada1999@gmail.com'  # Your email address
smtp_password = 'nczy qogr vofn kmcv'  # Your email password

# Function to send email
def send_email(to_address, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_address, text)
        server.quit()
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

# Function to fetch and process attendance data
def fetch_and_process_attendance():
    try:
        # Attempt to connect to the database
        engine = create_engine(database_url)
        connection = engine.connect()

        # Query to fetch attendance data for the given date
        table_name = "attend_app_count_number"
        employee_details_table = "attend_app_employee_details"
        date_input = datetime.now().strftime('%d/%m/%Y') #input("Enter the date (dd/mm/yyyy): ")

        # Validate the date format
        date_object = datetime.strptime(date_input, '%d/%m/%Y')
        formatted_date = date_object.strftime('%d/%m/%Y')

        query = f"""
            SELECT * FROM {table_name}
            WHERE DateString = '{formatted_date}'
        """
        df = pd.read_sql(query, connection)

        # Filter based on null or '--:--' entries in INTime
        filtered_df = df[(df['intime'].isnull()) | (df['intime'] == '--:--')]

        if filtered_df.empty:
            print(f"No people found with missing entries on {date_input}")
        else:
            emp_codes_with_issues = filtered_df['empcode'].tolist()
            print(f"Empcodes with missing entries on {date_input}: {emp_codes_with_issues}")

            # Query to fetch email addresses for the employees with missing INTime
            emp_codes_str = "','".join(emp_codes_with_issues)
            email_query = f"""
                SELECT emp_code, email FROM {employee_details_table}
                WHERE emp_code IN ('{emp_codes_str}')
            """
            email_df = pd.read_sql(email_query, connection)

            # Send emails to employees with missing INTime
            for index, row in email_df.iterrows():
                emp_code = row['emp_code']
                email = row['email']
                subject = "Missing In Time Alert"
                body= f"""Dear,\n
I hope you're well.\n
It appears that your attendance entry for {date_input} is missing. Could you please contact the HR department at your earliest convenience to get it updated?
If you have any questions, feel free to reach out.\n
Thank you for your cooperation.\n
Best Regards,\n
OrangeDataTech Pvt Ltd
"""

                send_email(email, subject, body)

            print(f"Emails sent to employees with missing INTime on {date_input}")

            # Print the DataFrame for verification
            print("Data for the specified date:")
            print(df)

    except exc.SQLAlchemyError as sql_error:
        print(f"SQLAlchemy error occurred: {sql_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

# # Schedule the task
# schedule.every().day.at("17:45").do(fetch_and_process_attendance)
# schedule.every().day.at("17:50").do(fetch_and_process_attendance)

# # Keep the script running and check the schedule
# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Wait for one minute before checking the schedule again
