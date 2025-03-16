# Trip Budget System
Project Link: https://github.com/premkumark20/Trip_Budget_System

## Overview
Trip Budget System is a comprehensive web application designed to help travelers manage their transportation budgets efficiently when planning trips across Tamil Nadu, India. The system provides detailed cost comparisons between bus and train options, calculates journey distances, and offers an intuitive interface for making informed travel decisions.

## Features

### Core Functionality
- **Route Planning**: Calculate distances between any two locations in Tamil Nadu
- **Cost Comparison**: Compare various bus and train options with detailed pricing
- **Budget Analysis**: Filter transportation options based on your specified budget
- **Interactive Maps**: Visualize your journey route using Google Maps integration
- **Offline Support**: Basic functionality available without internet connection

### Transportation Options
- **Bus Categories**: Multiple bus types including Luxury AC Sleeper, Semi Sleeper AC, Non AC Seater, and more
- **Train Classes**: Various train classes including First Class AC, Sleeper Class, AC Chair Car, and more
- **Timing Options**: Comprehensive departure schedules for planning convenience

## Demo

*Note: This is a local web application that requires setup before use. The URL `http://127.0.0.1:5000/` will only work after you've completed the installation steps below and started the application on your local machine.*

- Local Flask version: http://localhost:5000
- GitHub Pages version: [https://Trip_Budget_System.github.com](https://trip-budget-system.onrender.com)
- Live Demo: [Trip Budget System.render.api](https://trip-budget-system.onrender.com)

## Technical Architecture

### Backend
- Flask web framework for routing and application logic
- SQLite database for storing transportation data
- RESTful approach for handling form submissions and data retrieval

### Frontend
- Responsive design with mobile-first approach
- Interactive UI elements for enhanced user experience
- Real-time budget calculations and validations

### APIs & External Services
- Google Maps Directions API for distance calculations and route visualization
- Environment variable configuration for secure credential management

## Installation

### Prerequisites
- Python 3.7+
- pip package manager
- Google Maps API key (Get one from [Google Cloud Platform](https://console.cloud.google.com/))

### Setup Process
1. Clone the repository:
   ```
   git clone https://github.com/premkumark20/Trip_Budget_System.git
   cd Trip_Budget_System
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root with:
   ```
   SECRET_KEY=your_secure_secret_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   FLASK_DEBUG=True  # Set to False in production
   ```

5. Initialize the database:
   ```
   python app.py
   ```
   Note: Sample transportation data will be automatically populated on first run.

## Usage Guide

1. Start the application:
   ```
   python app.py
   ```

2. Access the web interface at:
   ```
   http://127.0.0.1:5000/
   ```
   This URL will only work on your local machine after starting the application.

3. Enter journey details:
   - Origin location (e.g., "Chennai", "Madurai", "Coimbatore")
   - Destination (e.g., "Tirunelveli", "Salem", "Kanchipuram")
   - Number of travelers
   - Budget allocation (optional)

4. Explore transportation options:
   - View journey distance and route map
   - Compare bus and train options
   - Filter by budget constraints
   - Examine detailed cost breakdowns

## Project Structure
```
Trip_Budget_System/
├── app.py                # Main application file
├── database.py           # Database connection and initialization
├── budget_data.py        # Sample data generation
├── static/
│   └── style.css         # CSS styles
├── templates/
│   └── index.html        # HTML template
├── .env                  # Environment variables (not committed)
├── .gitignore            # Git ignore configuration
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Deployment Options

### Local Development Server
The application runs on Flask's built-in development server by default, accessible at `http://127.0.0.1:5000/`.

### Production Deployment
For production deployment, consider:

1. **Gunicorn/WSGI Server**:
   ```
   gunicorn app:app
   ```

2. **Docker Containerization**:
   Create a Dockerfile and deploy using Docker.

3. **Cloud Platforms**:
   Deploy to services like Heroku, AWS, or Google Cloud Platform.

## Available Cities
The system includes transportation data for major Tamil Nadu cities including:
- Chennai
- Coimbatore
- Madurai
- Tiruchirappalli
- Salem
- Tirunelveli
- Thoothukudi
- Erode
- Vellore
- Dindigul
- Thanjavur
- Ranipet
- Sivakasi
- Karur
- Udhagamandalam
- Hosur
- Nagercoil
- Kanchipuram
- Kumbakonam
- Tirupur

## Performance Considerations
- Efficient database queries for rapid transportation cost retrieval
- Graceful degradation when network connectivity is limited
- Optimized for both desktop and mobile experiences

## Troubleshooting

### Common Issues

1. **Database Errors**:
   - Ensure SQLite is working correctly on your system
   - Check if the database file has proper write permissions

2. **Google Maps API Issues**:
   - Verify your API key is valid and has the Directions API enabled
   - Check for any quota limitations or restrictions

3. **No Transportation Options Showing**:
   - Ensure you're entering valid Tamil Nadu city names
   - Try different city combinations as not all routes may be available

### Debug Mode
For development and troubleshooting, ensure `FLASK_DEBUG=True` is set in your `.env` file.

## Future Enhancements
- User accounts for saving favorite routes
- Historical price tracking
- Additional transportation options (flights, car rentals)
- Multi-city trip planning
- Accommodation recommendations
- Weather integration for trip planning
- Support for other Indian states beyond Tamil Nadu

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Developer
Developed by Premkumar K

## Acknowledgements
- Google Maps Platform for providing the distance calculation API
- Flask community for the excellent web framework
- Contributors to the open-source libraries used in this project