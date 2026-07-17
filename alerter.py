import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Scanner function imported
from scanner import check_low_stock_items

def send_email_alert():
    # Scanner is run to see if there are any low stock items
    low_stock_items = check_low_stock_items()

    