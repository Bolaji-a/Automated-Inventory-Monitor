from fastapi import FastAPI
from scanner import check_low_stock_items
from alerter import send_email_alert