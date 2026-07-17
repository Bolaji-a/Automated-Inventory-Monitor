# Automated Supply Chain Inventory Monitor

An asynchronous backend microservice built with **Python**, **FastAPI**, and **SQLite** designed to monitor real-time stock levels across distributed warehouse nodes and trigger instant, secure email notifications when inventory dips below safety thresholds.

This project demonstrates clean coding practices, relational database normalization, asynchronous background task execution, and secure credential handling via environment abstraction.

---

## 🛠️ Tech Stack & Key Architectures

*   **Language:** Python 3.x
*   **Web Framework:** FastAPI (Asynchronous REST API)
*   **Database:** SQLite3 (Relational database engine)
*   **Protocol:** SMTP (Simple Mail Transfer Protocol via `smtplib`)
*   **Configurations:** Environment variables via `python-dotenv`

---

## 📐 System Architecture & Database Design

The database schema is fully normalized to eliminate redundancy. Rather than repeating warehouse metadata across inventory lines, items are bound dynamically via foreign key relations.

### Schema Blueprint

*   **`warehouses` Table:** Manages physical node footprints (ID, Name, Location).
*   **`inventory` Table:** Manages current stock levels relative to localized limits (ID, Warehouse_ID, Item_Name, Quantity, Safety_Threshold).

```text
  [ Warehouses Table ] 1  ───  * [ Inventory Table ]
  (id, name, location)            (id, warehouse_id, item_name, quantity, threshold)
```

---

## 🚀 API Endpoints

FastAPI automatically generates interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Microservice system status check |
| `GET` | `/alerts` | Scans the database and returns a list of all low-stock items in standard JSON |
| `POST` | `/trigger-alert` | Executes an active DB query scan and immediately dispatches SMTP email alerts |

---

## 💻 Local Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Bolaji-a/automated-inventory-monitor.git
cd automated-inventory-monitor
```

### 2. Set up a Virtual Environment
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory:
```env
SENDER_EMAIL=your_gmail_address@gmail.com
RECEIVER_EMAIL=your_recipient_address@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```
*(Note: `.env` is listed inside `.gitignore` and will never be pushed to public repository to maintain system security.)*

### 5. Initialize the Database & Seed Mock Data
Before starting the API, run the database initialization script to create tables and load sample supply chain items:
```bash
python database.py
```

### 6. Spin Up the FastAPI Server
```bash
uvicorn main:app --reload
```
Navigate to `http://127.0.0.1:8000/docs` to test the API endpoints interactively!
