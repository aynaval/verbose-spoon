import sqlite3

# Connect to SQLite database (create if doesn't exist)
conn = sqlite3.connect("tracking.db")
cursor = conn.cursor()

# Drop if exists
cursor.execute("DROP TABLE IF EXISTS ORDER_TRACKING")
cursor.execute("DROP TABLE IF EXISTS UPS_TRACKING")

# Create ORDER_TRACKING table
cursor.execute("""
CREATE TABLE ORDER_TRACKING (
    customer_name TEXT,
    customer_account_number INTEGER,
    order_number TEXT PRIMARY KEY,
    product_name TEXT,
    quantity TEXT,
    date_of_order TEXT,
    order_status TEXT,
    delivery_date TEXT,
    tracking_number TEXT, -- comma-separated string
    num_tracking_numbers INTEGER
)
""")

# Create UPS_TRACKING table
cursor.execute("""
CREATE TABLE UPS_TRACKING (
    tracking_number TEXT PRIMARY KEY,
    delivery_status TEXT,
    last_scanned_location TEXT,
    order_status TEXT,
    delivery_date TEXT,
    delivery_time TEXT,
    PO_number TEXT
)
""")

# Insert dummy ORDER_TRACKING data
order_data = [
    ("John Doe", 123456, "ORD123456", "PainReliefX", "2", "2025-04-10", "Shipped", "2025-04-15", "TRK001,TRK002", 2),
    ("Jane Smith", 789012, "ORD789012", "AllergyAway", "1", "2025-04-11", "In Transit", "2025-04-16", "TRK003", 1),
    ("Alan Parker", 345678, "ORD345678", "VitaBoost", "3", "2025-04-12", "Delivered", "2025-04-13", "", 0),
    ("Sophia Johnson", 456789, "ORD456789", "ImmunoMax", "4", "2025-04-13", "Processing", "2025-04-17", "TRK004,TRK005", 2),
    ("Michael Lee", 567890, "ORD567890", "PainReliefX", "1", "2025-04-14", "Shipped", "2025-04-19", "TRK006", 1),
    ("Emily Davis", 678901, "ORD678901", "VitaBoost", "2", "2025-04-15", "In Transit", "2025-04-20", "TRK007,TRK008,TRK009", 3),
    ("Chris Martin", 789901, "ORD789901", "AllergyAway", "2", "2025-04-16", "Delivered", "2025-04-18", "TRK010", 1),
    ("Lily White", 890012, "ORD890012", "ImmunoMax", "1", "2025-04-17", "Shipped", "2025-04-21", "TRK011,TRK012", 2),
    ("Ryan Clark", 901234, "ORD901234", "PainReliefX", "5", "2025-04-18", "In Transit", "2025-04-23", "TRK013", 1),
    ("Olivia Scott", 234567, "ORD234567", "VitaBoost", "3", "2025-04-19", "Processing", "2025-04-24", "TRK014,TRK015", 2),
    ("Daniel Harris", 345789, "ORD345789", "AllergyAway", "4", "2025-04-20", "Shipped", "2025-04-25", "TRK016,TRK017", 2),
    ("Grace Lewis", 456890, "ORD456890", "ImmunoMax", "2", "2025-04-21", "Delivered", "2025-04-22", "TRK018", 1),
    ("William Walker", 567901, "ORD567901", "PainReliefX", "3", "2025-04-22", "In Transit", "2025-04-27", "TRK019,TRK020,TRK021", 3),
    ("Charlotte Allen", 678912, "ORD678912", "VitaBoost", "1", "2025-04-23", "Shipped", "2025-04-28", "TRK022", 1)
]
cursor.executemany("""
INSERT INTO ORDER_TRACKING VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", order_data)

# Insert dummy UPS_TRACKING data
ups_data = [
    ("TRK001", "In Transit", "Facility A", "Shipped", "2025-04-15", "14:00", "PO111"),
    ("TRK002", "Delivered", "Facility B", "Delivered", "2025-04-14", "09:00", "PO111"),
    ("TRK003", "In Transit", "Facility X", "In Transit", "2025-04-16", "11:00", "PO222"),
    ("TRK004", "Processing", "Facility C", "Processing", "2025-04-17", "16:00", "PO333"),
    ("TRK005", "Shipped", "Facility D", "Shipped", "2025-04-18", "10:00", "PO333"),
    ("TRK006", "Delivered", "Facility E", "Delivered", "2025-04-19", "18:00", "PO444"),
    ("TRK007", "In Transit", "Facility F", "In Transit", "2025-04-20", "15:00", "PO555"),
    ("TRK008", "Shipped", "Facility G", "Shipped", "2025-04-21", "08:00", "PO555"),
    ("TRK009", "Delivered", "Facility H", "Delivered", "2025-04-22", "13:00", "PO666"),
    ("TRK010", "Shipped", "Facility I", "Shipped", "2025-04-23", "09:30", "PO777"),
    ("TRK011", "In Transit", "Facility J", "In Transit", "2025-04-24", "14:30", "PO888"),
    ("TRK012", "Delivered", "Facility K", "Delivered", "2025-04-25", "17:00", "PO888"),
    ("TRK013", "Delivered", "Facility L", "Delivered", "2025-04-26", "12:00", "PO999"),
    ("TRK014", "Shipped", "Facility M", "Shipped", "2025-04-27", "10:15", "PO1000"),
    ("TRK015", "In Transit", "Facility N", "In Transit", "2025-04-28", "16:45", "PO1001")
]
cursor.executemany("""
INSERT INTO UPS_TRACKING VALUES (?, ?, ?, ?, ?, ?, ?)
""", ups_data)

# Commit changes and close the connection
conn.commit()
conn.close()
