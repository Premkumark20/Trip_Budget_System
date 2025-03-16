import sqlite3
from database import get_db_connection
import random

# Tamil Nadu locations
TN_CITIES = [
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", 
    "Tirunelveli", "Thoothukudi", "Erode", "Vellore", "Dindigul", 
    "Thanjavur", "Ranipet", "Sivakasi", "Karur", "Udhagamandalam", 
    "Hosur", "Nagercoil", "Kanchipuram", "Kumbakonam", "Tirupur"
]

# Bus timings - different from train timings
BUS_TIMINGS = [
    "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", 
    "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", 
    "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", 
    "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", 
    "22:00", "22:30", "23:00", "23:30"
]

# Bus categories
BUS_CATEGORIES = [
    "Luxury AC Sleeper", "Semi Sleeper AC", "Non AC Seater", 
    "Ultra Deluxe", "AC Seater", "Deluxe", "Super Deluxe", 
    "Volvo AC", "Premium AC", "Economy", "Express Non-AC"
]

# Train categories
TRAIN_CATEGORIES = [
    "First Class AC", "Second Class AC", "Sleeper Class",
    "AC Chair Car", "Executive Class", "First Class", 
    "General", "Vistadome AC", "Third AC", "Premium AC",
    "Economy AC"
]

def generate_comprehensive_dataset(count_per_type=1000):
    """Generate 1000 entries each for bus and train routes with all categories for each city pair."""
    bus_data = []
    train_data = []
    
    # Create all possible city pairs (both directions)
    city_pairs = []
    for from_city in TN_CITIES:
        for to_city in TN_CITIES:
            if from_city != to_city:  # Don't create routes from a city to itself
                city_pairs.append((from_city, to_city))
    
    # For buses - ensure all categories are represented for each city pair
    bus_entries = 0
    pair_index = 0
    
    while bus_entries < count_per_type:
        # Get the current city pair (cycling through all pairs)
        from_city, to_city = city_pairs[pair_index % len(city_pairs)]
        pair_index += 1
        
        # Calculate a consistent distance factor for this city pair
        distance_factor = 0.8 + (hash(from_city + to_city) % 40) / 100
        
        # Cycle through all categories for each city pair
        for category in BUS_CATEGORIES:
            # Generate appropriate costs based on category
            if "Luxury" in category or "AC" in category:
                cost = min(max(round(250 * distance_factor + random.randint(10, 100), 0), 180), 350)
            else:
                cost = min(max(round(150 * distance_factor + random.randint(10, 50), 0), 80), 250)
            
            # Add multiple timing options for each category and city pair
            timings_to_use = random.sample(BUS_TIMINGS, min(3, len(BUS_TIMINGS)))
            for timing in timings_to_use:
                unique_entry = (from_city, to_city, category, float(cost), timing)
                
                # Only add if this exact entry doesn't exist yet
                if unique_entry not in bus_data:
                    bus_data.append(unique_entry)
                    bus_entries += 1
                    
                    if bus_entries >= count_per_type:
                        break
            
            if bus_entries >= count_per_type:
                break
        
        if bus_entries >= count_per_type:
            break
    
    # For trains - ensure all categories are represented for each city pair
    train_entries = 0
    pair_index = 0
    
    while train_entries < count_per_type:
        # Get the current city pair (cycling through all pairs)
        from_city, to_city = city_pairs[pair_index % len(city_pairs)]
        pair_index += 1
        
        # Calculate a consistent distance factor for this city pair
        distance_factor = 0.8 + (hash(from_city + to_city) % 40) / 100
        
        # Cycle through all categories for each city pair
        for category in TRAIN_CATEGORIES:
            # Generate appropriate costs based on category
            if "First Class" in category or "Executive" in category:
                cost = min(max(round(350 * distance_factor + random.randint(20, 150), 0), 300), 500)
            elif "AC" in category:
                cost = min(max(round(250 * distance_factor + random.randint(20, 100), 0), 200), 400)
            else:
                cost = min(max(round(180 * distance_factor + random.randint(20, 80), 0), 120), 300)
            
            # Generate multiple train timings for each category and city pair
            for _ in range(min(3, 5)):
                hour = random.randint(5, 23)
                minute = random.choice([0, 15, 30, 45])
                timing = f"{hour:02d}:{minute:02d}"
                
                unique_entry = (from_city, to_city, category, float(cost), timing)
                
                # Only add if this exact entry doesn't exist yet
                if unique_entry not in train_data:
                    train_data.append(unique_entry)
                    train_entries += 1
                    
                    if train_entries >= count_per_type:
                        break
            
            if train_entries >= count_per_type:
                break
        
        if train_entries >= count_per_type:
            break
    
    # Trim if we ended up with more than requested
    return bus_data[:count_per_type], train_data[:count_per_type]

def check_data_exists():
    """Check if data already exists in the tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM bus_costs")
    bus_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM train_costs")
    train_count = cursor.fetchone()[0]
    
    conn.close()
    
    return bus_count > 0 and train_count > 0

def clear_existing_data():
    """Clear any existing data from the tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM bus_costs")
    cursor.execute("DELETE FROM train_costs")
    
    conn.commit()
    conn.close()
    print("Existing data cleared.")

def insert_data():
    """Insert transportation data into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate exactly 1000 entries for each type
    bus_data, train_data = generate_comprehensive_dataset(1000)
    
    # Insert bus data
    for data in bus_data:
        cursor.execute(
            "INSERT INTO bus_costs (from_place, to_place, category, cost, timing) VALUES (?, ?, ?, ?, ?)",
            data
        )
    
    # Insert train data
    for data in train_data:
        cursor.execute(
            "INSERT INTO train_costs (from_place, to_place, category, cost, timing) VALUES (?, ?, ?, ?, ?)",
            data
        )
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(bus_data)} bus routes and {len(train_data)} train routes")

def check_and_insert_data(force_update=False):
    """Check if data exists and insert if needed or if force_update is True."""
    if not check_data_exists() or force_update:
        if force_update and check_data_exists():
            print("Forcing update: Clearing existing data...")
            clear_existing_data()
        
        print("Inserting comprehensive sample data...")
        insert_data()
        print("Data insertion complete.")
    else:
        print("Data already exists in database. Use force_update=True to replace it.")

if __name__ == "__main__":
    # Can be run independently to insert data
    # Set force_update=True to replace existing data
    check_and_insert_data(force_update=True)