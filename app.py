import os
import sqlite3
import requests
from requests.exceptions import RequestException
from flask import Flask, request, render_template, flash, redirect, url_for
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key')

# Get Google Maps API key from environment variables
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyC3hCbbPBjqUav_TJEjfry1q2-i67CIN2k')

# Database path
DATABASE = 'database.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_directions(from_place, to_place):
    """Fetches route distance from Google Maps API, handles errors when offline."""
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={from_place}&destination={to_place}&key={GOOGLE_MAPS_API_KEY}'
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        directions = response.json()

        if directions['status'] == 'OK':
            distance = directions['routes'][0]['legs'][0]['distance']['text']
            return distance
        elif directions['status'] == 'ZERO_RESULTS':
            return "No route found between these locations"
        else:
            return f"Error: {directions['status']}"

    except RequestException:
        return "Internet not available"

def get_costs(transport_type, from_place, to_place, sort_by_budget=False, budget=0, total_members=1):
    """Fetches transportation costs from the database."""
    try:
        conn = get_db_connection()
        
        # Base query
        query = f"SELECT category, cost, timing FROM {transport_type}_costs WHERE from_place = ? AND to_place = ?"
        
        # Add budget filter if needed
        params = (from_place, to_place)
        if budget > 0 and total_members > 0:
            # Filter by per-person cost to stay within budget
            max_cost_per_person = budget / total_members
            query += f" AND cost <= ?"
            params = (from_place, to_place, max_cost_per_person)
        
        # Add sorting
        if sort_by_budget:
            query += " ORDER BY cost ASC"
        else:
            query += " ORDER BY timing ASC"

        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Also get all costs to check if any are over budget
        if budget > 0 and total_members > 0:
            cursor.execute(f"SELECT MIN(cost) FROM {transport_type}_costs WHERE from_place = ? AND to_place = ?", 
                          (from_place, to_place))
            min_cost_result = cursor.fetchone()[0]
            min_cost = float(min_cost_result) if min_cost_result is not None else None
            
            cursor.execute(f"SELECT MAX(cost) FROM {transport_type}_costs WHERE from_place = ? AND to_place = ?", 
                          (from_place, to_place))
            max_cost_result = cursor.fetchone()[0]
            max_cost = float(max_cost_result) if max_cost_result is not None else None
            
            conn.close()
            return results, min_cost, max_cost
        else:
            conn.close()
            return results, None, None
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if budget > 0 and total_members > 0:
            return [], None, None
        else:
            return [], None, None

def check_minimum_cost(from_place, to_place):
    """Get the absolute minimum cost across all transportation options."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query for minimum bus cost
        cursor.execute("SELECT MIN(cost) FROM bus_costs WHERE from_place = ? AND to_place = ?", 
                      (from_place, to_place))
        min_bus_cost_result = cursor.fetchone()[0]
        min_bus_cost = float(min_bus_cost_result) if min_bus_cost_result is not None else None
        
        # Query for minimum train cost
        cursor.execute("SELECT MIN(cost) FROM train_costs WHERE from_place = ? AND to_place = ?", 
                      (from_place, to_place))
        min_train_cost_result = cursor.fetchone()[0]
        min_train_cost = float(min_train_cost_result) if min_train_cost_result is not None else None
        
        conn.close()
        
        # Determine the overall minimum
        if min_bus_cost is None and min_train_cost is None:
            return None
        elif min_bus_cost is None:
            return min_train_cost
        elif min_train_cost is None:
            return min_bus_cost
        else:
            return min(min_bus_cost, min_train_cost)
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission and calculates transportation costs."""
    # Get form data with validation
    from_place = request.form.get('from', '').strip()
    to_place = request.form.get('to', '').strip()
    
    try:
        total_members = int(request.form.get('total_members', 0) or 0)
    except ValueError:
        total_members = 0
        
    try:
        budget = float(request.form.get('budget', 0) or 0)
    except ValueError:
        budget = 0

    # Validate inputs
    if not from_place or not to_place:
        flash("Please provide valid 'from' and 'to' locations.", "error")
        return render_template('index.html')

    # Get distance information
    distance = get_directions(from_place, to_place)
    if distance.startswith("Error"):
        flash(distance, "error")
        return render_template('index.html')

    # Check if budget is provided but insufficient
    budget_message = None
    if budget > 0 and total_members > 0:
        min_cost_per_person = check_minimum_cost(from_place, to_place)
        if min_cost_per_person is not None:
            total_min_cost = min_cost_per_person * total_members

    # Connect to database and get costs
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get bus cost
        cursor.execute("SELECT cost FROM bus_costs WHERE from_place = ? AND to_place = ? ORDER BY cost ASC LIMIT 1", 
                      (from_place, to_place))
        bus_result = cursor.fetchone()
        bus_cost_per_person = float(bus_result[0]) if bus_result else None

        # Get train cost
        cursor.execute("SELECT cost FROM train_costs WHERE from_place = ? AND to_place = ? ORDER BY cost ASC LIMIT 1", 
                      (from_place, to_place))
        train_result = cursor.fetchone()
        train_cost_per_person = float(train_result[0]) if train_result else None

        conn.close()

        # Calculate total costs
        bus_total_cost = bus_cost_per_person * total_members if bus_cost_per_person and total_members else None
        train_total_cost = train_cost_per_person * total_members if train_cost_per_person and total_members else None

        # Check budget again
        if budget > 0 and total_members > 0:
            min_cost = min(
                float('inf') if bus_total_cost is None else bus_total_cost,
                float('inf') if train_total_cost is None else train_total_cost
            )
            
            if min_cost != float('inf') and budget < min_cost:
                budget_message = "You will need additional funds to proceed with this tour."
                flash(budget_message, "error")
        
        # Check if we have any transport options available
        if bus_cost_per_person is None and train_cost_per_person is None:
            flash(f"No transportation options found from {from_place} to {to_place}", "info")
                
        return render_template(
            'index.html',
            from_place=from_place,
            to_place=to_place,
            directions=distance,
            kilometers=distance,
            bus_cost_per_person=bus_cost_per_person,
            train_cost_per_person=train_cost_per_person,
            bus_total_cost=bus_total_cost,
            train_total_cost=train_total_cost,
            budget_message=budget_message,
            total_members=total_members,
            budget=budget,
            google_maps_api_key=GOOGLE_MAPS_API_KEY
        )
        
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "error")
        return render_template('index.html')

@app.route('/bus')
def bus():
    """Displays bus costs based on form data."""
    from_place = request.args.get('from')
    to_place = request.args.get('to')
    
    try:
        budget = float(request.args.get('budget', 0) or 0)
    except ValueError:
        budget = 0
    
    try:
        total_members = int(request.args.get('total_members', 1) or 1)
    except ValueError:
        total_members = 1
        
    if not from_place or not to_place:
        flash("Missing location information", "error")
        return redirect(url_for('index'))
        
    sort_by_budget = budget > 0
    
    # Get costs with budget filter
    costs, min_cost, max_cost = get_costs('bus', from_place, to_place, sort_by_budget, budget, total_members)
    
    budget_message = None
    if not costs and min_cost is None:
        flash(f"No bus routes found from {from_place} to {to_place}", "info")
    elif budget > 0 and min_cost is not None:
        # Check if we filtered out any options due to budget
        min_total_cost = min_cost * total_members
        if budget < min_total_cost:
            flash(f"Your budget of ₹{budget} is insufficient. The minimum cost for bus travel is ₹{min_total_cost:.2f}", "error")
            budget_message = "You will need additional funds to proceed with this tour."
            flash(budget_message, "error")
        elif max_cost * total_members > budget:
            # Some options are within budget but not all
            flash(f"Some bus options are within your budget of ₹{budget}, but not all. Options with higher costs are not shown.", "info")
        
    return render_template(
        'index.html',
        costs=costs,
        transport_type='bus',
        from_place=from_place,
        to_place=to_place,
        budget=budget,
        total_members=total_members,
        budget_message=budget_message
    )

@app.route('/train')
def train():
    """Displays train costs based on form data."""
    from_place = request.args.get('from')
    to_place = request.args.get('to')
    
    try:
        budget = float(request.args.get('budget', 0) or 0)
    except ValueError:
        budget = 0
    
    try:
        total_members = int(request.args.get('total_members', 1) or 1)
    except ValueError:
        total_members = 1
        
    if not from_place or not to_place:
        flash("Missing location information", "error")
        return redirect(url_for('index'))
        
    sort_by_budget = budget > 0
    
    # Get costs with budget filter
    costs, min_cost, max_cost = get_costs('train', from_place, to_place, sort_by_budget, budget, total_members)
    
    budget_message = None
    if not costs and min_cost is None:
        flash(f"No train routes found from {from_place} to {to_place}", "info")
    elif budget > 0 and min_cost is not None:
        # Check if we filtered out any options due to budget
        min_total_cost = min_cost * total_members
        if budget < min_total_cost:
            flash(f"Your budget of ₹{budget} is insufficient. The minimum cost for train travel is ₹{min_total_cost:.2f}", "error")
            budget_message = "You will need additional funds to proceed with this tour."
            flash(budget_message, "error")
        elif max_cost * total_members > budget:
            # Some options are within budget but not all
            flash(f"Some train options are within your budget of ₹{budget}, but not all. Options with higher costs are not shown.", "info")
        
    return render_template(
        'index.html',
        costs=costs,
        transport_type='train',
        from_place=from_place,
        to_place=to_place,
        budget=budget,
        total_members=total_members,
        budget_message=budget_message
    )

if __name__ == '__main__':
    # Import database module to ensure tables exist
    import database
    import budget_data
    
    # Create database and tables if they don't exist
    database.init_db()
    
    # Insert data if tables are empty
    budget_data.check_and_insert_data()
    
    # Set debug mode based on environment
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)