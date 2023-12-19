import requests
from datetime import datetime
import pytz
import configparser
from timezones import city_timezone_map

config = configparser.ConfigParser()
config.read('config.ini')

base_url = config['source']['BASE_URL']
api_key = config['keys']['API_KEY']
current_city = config['data']['CITY_NAME']



def convert_unix_timestamp_to_local_time(timestamp):
    try:
        timestamp = int(timestamp)
        utc_time = datetime.utcfromtimestamp(timestamp)

        # Get the user's local time zone
        user_timezone = pytz.timezone(city_timezone_map.get(current_city, 'UTC'))
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(user_timezone)

        return local_time.strftime('%I:%M %p %Z').lstrip("0")

    except ValueError:
        return "Invalid timestamp"


# API endpoint and parameters
params = {
    'q': current_city,
    'appid': api_key,
    'units': 'imperial',  # You can change to 'imperial' for Fahrenheit
}

unit_value = 'F' if params.get('units') == 'imperial' else 'C'

# Make the API request
response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()

    # Extract relevant information from the response
    temperature = data['main']['temp']
    weather_description = data['weather'][0]['description']
    feels_like = data['main']['feels_like']
    day_high = data['main']['temp_max']
    day_low = data['main']['temp_min']
    humidity = data['main']['humidity']
    sunrise = convert_unix_timestamp_to_local_time(data['sys']['sunrise'])
    sunset = convert_unix_timestamp_to_local_time(data['sys']['sunset'])

else:
    print("Error fetching data. Review your supplied values.")



if __name__ == '__main__':
    print(f"Current Weather: {current_city}\n")
    print(f"Temperature: {temperature:.1f}° {unit_value}")
    print(f"Feels like: {feels_like:.1f}° {unit_value}")
    print(f"Humidity: {humidity} %")
    print(f"Description: {weather_description}\n")

    print(f"High temp: {day_high:.1f}° {unit_value}")
    print(f"Low temp: {day_low:.1f}° {unit_value}")

    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
