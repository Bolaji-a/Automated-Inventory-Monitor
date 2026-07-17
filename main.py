from fastapi import FastAPI
from scanner import check_low_stock_items
from alerter import send_email_alert

# Initialize FastAPI app
app = FastAPI(
    title ="Automated Inventory Monitoring System",
    description="This API monitors inventory levels across multiple warehouse nodes and sends alerts for low stock items.",
    version="1.0.0"
)

# Define a basic home route
@app.get("/")
def home():
    return{
        "status": "online",
        "message": "Automated Inventory Monitoring System is running.",
        "docs_url": "/docs" # for automated documentation
    }

# Define a route to trigger the inventory scan and email alert
@app.get("/alerts")
def get_current_alerts():
    """
    Fetches and returns current low-stock items across all warehouse nodes.
    """
    raw_alerts = check_low_stock_items()

    # Format the raw alerts into a structured response
    formatted_alerts = []
    for row in raw_alerts:
        formatted_alerts.append({
            "warehouse_name": row[3],
            "item_name": row[0],
            "quantity": row[1],
            "safety_threshold": row[2]
        })

    return {
        "alert_count": len(formatted_alerts),
        "low_stock_items": formatted_alerts
    }

# Route to trigger the email alert manually
@app.post("/send-alerts")
def trigger_email_alert():
    """
    Triggers the email alert for low-stock items after running a scan
    """
    try:
        send_email_alert()
        return {
            "status": "success",
            "message": "Email alert process executed. Check logs for details."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email alert: {str(e)}"
        }