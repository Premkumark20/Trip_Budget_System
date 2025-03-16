🚆 Trip Budget System 🚌
A smart travel cost estimator for bus and train journeys in Tamil Nadu.

📌 Project Overview
The Trip Budget System is a Python-based application that helps users estimate bus and train travel costs across different cities in Tamil Nadu. It fetches fare details, available routes, and travel timings from a structured SQLite database.

✅ Key Features:
✔ City-to-City Travel Costs – Covers major Tamil Nadu destinations.
✔ Bus & Train Fare Estimation – Includes different seat categories.
✔ Real-Time Schedule Information – Shows available departure times.
✔ Budget Calculation – Estimates total travel expenses.
✔ Web-Based UI – Simple, interactive interface using Flask.

📂 Project Structure
php
Copy
Edit
Trip_Budget_System/
│── app.py               # Main application (Flask backend)
│── database.py          # Database connection and initialization
│── budget_data.py       # Travel cost dataset and data insertion
│── requirements.txt     # List of dependencies
│── README.md            # Project documentation
│── .gitignore           # Files to exclude from Git tracking
│
├── templates/           # HTML templates for web UI
│   ├── index.html       # Main user interface
│
├── static/              # Static assets (CSS, JS, images)
│   ├── style.css        # Stylesheet for the web UI
🚀 Installation & Setup
Follow these steps to set up and run the project locally.

1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/premkumark20/Trip_Budget_System.git
cd Trip_Budget_System

2️⃣ Create a Virtual Environment (Optional)
sh
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt

4️⃣ Initialize the Database
sh
Copy
Edit
python database.py

5️⃣ Insert Sample Data
sh
Copy
Edit
python budget_data.py

6️⃣ Run the Web Application
sh
Copy
Edit
python app.py
🔗 Open in Browser: http://127.0.0.1:5000/

🌐 Web Interface
The project features a user-friendly web interface built with Flask and HTML.

🏠 Homepage (index.html) – Users enter departure & destination details.
💰 Fare Results – Displays travel costs & available timings.
🎨 Styled UI (style.css) – Clean and modern interface for a better experience.

🛠 Technologies Used
Technology             | Purpose
--------------------------------------------------------------------
Python (Flask)	       | Backend logic & API handling
SQLite	               | Lightweight database for travel data storage
HTML, CSS (Bootstrap)  | Frontend user interface
JavaScript (Optional   |
Enhancements)	       | Interactive UI elements

📊 Future Enhancements
🔹 Live Train & Bus API Integration – Real-time fare updates
🔹 User Authentication – Login & profile management
🔹 Cost Comparison Feature – Compare different travel options dynamically
🔹 Mobile-Responsive Design – Optimize UI for mobile devices

🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch:
sh
Copy
Edit
git checkout -b feature-name
Commit your changes:
sh
Copy
Edit
git commit -m "Add new feature"
Push the branch:
sh
Copy
Edit
git push origin feature-name
Open a Pull Request 🚀

📜 License
This project is licensed under the MIT License.

⭐ Like this project? Give it a star on GitHub! 🌟