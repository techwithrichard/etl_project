# ETL Data Pipeline Project

## Project Overview
This project demonstrates a complete ETL (Extract, Transform, Load) data pipeline built with Python. It showcases data engineering concepts including data extraction from multiple sources, transformation processes, and loading into a data warehouse.

## What I Built
- **Data Extraction**: Multiple extractors for different data sources (Excel, APIs, web scraping, MySQL)
- **Data Transformation**: Data cleaning, validation, and transformation pipeline
- **Data Loading**: Structured loading into SQLite database with validation
- **Web Interface**: Flask-based dashboard to monitor and control the ETL process
- **Modular Architecture**: Clean separation of concerns with reusable components

## Why I Built This
This project demonstrates my understanding of:
- Data engineering principles and ETL workflows
- Python programming and object-oriented design
- Database design and SQL operations
- Web development with Flask
- API integration and web scraping
- Error handling and logging
- Testing and validation

## How Everything Works Together
The system follows a modular ETL architecture where each component has a single responsibility:
1. **Extractors** gather data from various sources
2. **Transformers** clean and prepare the data
3. **Loaders** store data in the warehouse
4. **Main Pipeline** orchestrates the entire process
5. **Web Interface** provides user control and monitoring

## Project Structure
```
etl_project/
├── extract/          # Data extraction modules
├── transform/        # Data transformation logic
├── load/            # Data loading and storage
├── warehouse/       # Data warehouse and validation
├── templates/       # Web interface templates
├── data/           # Sample data files
├── output/         # Processed data outputs
└── tests/          # Test files
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the web interface: `python app.py`
3. Execute ETL pipeline: `python etl_pipeline.py`

## Learning Journey
This commit history shows my step-by-step development process, from initial concept to a fully functional ETL system.
