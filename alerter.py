import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Scanner function imported
from scanner import check_low_stock_items

def send_email_alert():
    # Scanner is run to see if there are any low stock items
    low_stock_items = check_low_stock_items()

    # if there are no low stock items, an email is not required
    if not low_stock_items:
        print("No low stock items found. Email alert skipped.")
        return
    
    # Email configuration
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    # Confirming the env credentials
    if not all([sender_email, receiver_email, app_password]):
        print("❌ ERROR: Missing credentials in .env file.")
        return
    
    # Create the email message/container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"🚨 SYSTEM ALERT: {len(low_stock_items)} Low Stock Items Found!"

    # Create the email body
    email_body = "Hey there, Inventory Team\n\n"
    email_body += "The system has detected that the following items are running low in stock:\n\n"

    for row in low_stock_items:
       warehouse_name = row[3]
       item_name = row[0]
       quantity = row[1]
       safety_threshold = row[2]

       email_body += f"⚠️ [ALERT] Warehouse: {warehouse_name}\n"
       email_body += f"   - Item: {item_name}\n"
       email_body += f"   - Current Stock: {quantity}\n"
       email_body += f"   - Safety Threshold: {safety_threshold}\n"
       email_body += "-" * 40 + "\n"

    email_body += "\n\nPlease take the necessary actions to restock these items.\n\nBest regards,\nInventory Monitoring System"

    msg.attach(MIMEText(email_body, 'plain'))

    # Send the email using Gmail's SMTP server
    print(f"\n>>> CONNECTTING TO OUTBOUND MAIL SERVER ({os.getenv('SMTP_SERVER')}:{os.getenv('SMTP_PORT')})...<<<")
    try:

        server = smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
        # server.starttls() # Secure and encrypt the traffic/connection

        # Login to the SMTP server using the sender's email and app password
        server.login(sender_email, app_password)

        # Send MIME payload email
        server.send_message(msg)

        # Safely close the connection session
        server.quit()
        print(f"✅ Email alert sent successfully to {receiver_email}!")
    except Exception as e:
        print(f"❌ ERROR: Failed to send email alert. Details: {e}")

if __name__ == "__main__":
    send_email_alert();