 git# Installation Guide

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/techwithrichard/etl_project.git
   cd etl_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual credentials

4. **Run the project**
   ```bash
   # Start web dashboard
   python start.py
   
   # Or use CLI commands
   python cli.py dashboard
   python cli.py etl
   python cli.py test
   ```

## Environment Variables

Create a `.env` file with:
```
OPENWEATHER_API_KEY=your_api_key_here
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DATABASE=etl
```

## What You Need

- Python 3.8+
- MySQL database (optional - will use sample data if not available)
- OpenWeatherMap API key (optional - will use sample data if not available)
