import sqlite3
import os

# Database path
DATABASE = 'database.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with necessary tables."""
    # Check if database file exists
    db_exists = os.path.exists(DATABASE)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bus_costs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_place TEXT NOT NULL,
        to_place TEXT NOT NULL,
        category TEXT NOT NULL,
        cost REAL NOT NULL,
        timing TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS train_costs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_place TEXT NOT NULL,
        to_place TEXT NOT NULL,
        category TEXT NOT NULL,
        cost REAL NOT NULL,
        timing TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully")
    return not db_exists  # Return True if this was a new database