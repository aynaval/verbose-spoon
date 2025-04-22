from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("tracking.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/validate/account_number")
def validate_account_number(customer_account_number: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_name FROM ORDER_TRACKING WHERE customer_account_number = ?", (customer_account_number,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Customer account number not found")

    return {"customer_account_number": customer_account_number, "customer_name": result["customer_name"]}

@app.get("/delivery/po")
def check_delivery_status_by_po(po_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First get all tracking numbers for that PO
    cursor.execute("SELECT tracking_number FROM UPS_TRACKING WHERE PO_number = ?", (po_number,))
    rows = cursor.fetchall()
    if not rows:
        conn.close()
        raise HTTPException(status_code=404, detail="PO number not found")

    tracking_numbers = [row["tracking_number"] for row in rows]
    like_clauses = [f"%{trk}%" for trk in tracking_numbers]

    # Find order that contains any of the tracking numbers
    placeholders = " OR ".join(["tracking_number LIKE ?"] * len(like_clauses))
    cursor.execute(f"SELECT * FROM ORDER_TRACKING WHERE {placeholders}", like_clauses)
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Order not found for given PO number")

    tracking_list = result["tracking_number"].split(",") if result["tracking_number"] else []
    return {
        "customer_name": result["customer_name"],
        "order_number": result["order_number"],
        "product_name": result["product_name"],
        "order_status": result["order_status"],
        "delivery_date": result["delivery_date"],
        "tracking_number": tracking_list,
        "num_tracking_numbers": result["num_tracking_numbers"]
    }

@app.get("/delivery/order_number")
def check_delivery_status_by_order_number(order_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDER_TRACKING WHERE order_number = ?", (order_number,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Order not found")

    tracking_list = result["tracking_number"].split(",") if result["tracking_number"] else []
    return {
        "customer_name": result["customer_name"],
        "order_number": result["order_number"],
        "product_name": result["product_name"],
        "order_status": result["order_status"],
        "delivery_date": result["delivery_date"],
        "tracking_number": tracking_list,
        "num_tracking_numbers": result["num_tracking_numbers"]
    }

@app.get("/delivery/order_date")
def check_delivery_status_by_date(date_of_order: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDER_TRACKING WHERE date_of_order = ?", (date_of_order,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        raise HTTPException(status_code=404, detail="No orders found for this date")

    response = []
    for result in results:
        tracking_list = result["tracking_number"].split(",") if result["tracking_number"] else []
        response.append({
            "customer_name": result["customer_name"],
            "order_number": result["order_number"],
            "product_name": result["product_name"],
            "order_status": result["order_status"],
            "delivery_date": result["delivery_date"],
            "tracking_number": tracking_list,
            "num_tracking_numbers": result["num_tracking_numbers"]
        })

    return response
