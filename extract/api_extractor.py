import requests
import pandas as pd
import os
from datetime import datetime

def extract_from_weather_api(cities=None):
    """
    Extract weather data from OpenWeatherMap API for Kenyan cities
    Returns a DataFrame with current weather information
    """
    # kenya cities
    if cities is None:
        cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
    
    # Your API key
    api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
    # api_key="iuaybc98ewr98u98"
    
    all_weather_data = []
    
    for city in cities:
        try:
            # - sure city is a string, not a single character
            if not isinstance(city, str) or len(city) < 2:
                print(f"Skipping invalid city: {city}")
                continue
                
            # - API request for each city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},KE&appid={api_key}&units=metric"
            # http://api.openweathermap.org/data/2.5/weather?q={Nairobi},KE&appid={7398ba9119a049d09f563c3e1e72b405}&units=metric
            response = requests.get(url, timeout=10)
            print(response.status_code)
            print(response.text)
            
            if response.status_code == 200:
                data = response.json()
                print(data)
                # Extract relevant information
                weather_data = {
                    'city': city,
                    'country': 'Kenya',
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather_condition': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description'],
                    'wind_speed': data.get('wind', {}).get('speed'),
                    'cloudiness': data.get('clouds', {}).get('all'),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'api_response_code': response.status_code
                }
                
                all_weather_data.append(weather_data)
                print(f"Successfully extracted weather data for {city}")
                
            else:
                print(f"Failed to get data for {city}. Status code: {response.status_code}")
                # Add error record
                all_weather_data.append({
                    'city': city,
                    'country': 'Kenya',
                    'temperature': None,
                    'error': f"API Error: {response.status_code}",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'api_response_code': response.status_code
                })
                
        except Exception as e:
            print(f"Error extracting weather data for {city}: {e}")
            all_weather_data.append({
                'city': city,
                'country': 'Kenya',
                'temperature': None,
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # Create DataFrame
    if all_weather_data:
        df = pd.DataFrame(all_weather_data)
        print(f"Successfully extracted weather data for {len(df)} cities")
        return df
    else:
        print("No weather data could be extracted")
        # Return sample data as fallback
        return create_sample_weather_data()

def create_sample_weather_data():
    """
    Create sample weather data (fallback when API fails)
    """
    cities = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
    
    sample_data = []
    for city in cities:
        # Different weather patterns based on city
        if city == "Nairobi":
            temp = 22
            condition = "Cloudy"
        elif city == "Mombasa":
            temp = 28
            condition = "Sunny"
        elif city == "Kisumu":
            temp = 26
            condition = "Partly Cloudy"
        elif city == "Nakuru":
            temp = 20
            condition = "Light Rain"
        else:  # Eldoret
            temp = 18
            condition = "Cloudy"
        
        sample_data.append({
            'city': city,
            'country': 'Kenya',
            'temperature': temp,
            'humidity': 65 + (10 * (hash(city) % 5)),  # Randomish humidity
            'pressure': 1015,
            'weather_condition': condition,
            'weather_description': condition.lower(),
            'wind_speed': 3 + (hash(city) % 7),  # Randomish wind speed
            'cloudiness': 40 + (hash(city) % 40),  # Randomish cloudiness
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'api_response_code': 200,
            'is_sample_data': True
        })
    
    # print("Using sample weather data")
    return pd.DataFrame(sample_data)