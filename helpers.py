from sqlite3 import Error, connect
import requests
import os


def get_db_connection():
    DATABASE = 'tracker.db'
    connection = None
    try:
        connection = connect(DATABASE)
    except Error as e:
        print(f"the error '{e}' has occured")

    return connection


def getWeather(units, lat, lon):
    API_KEY = os.environ.get("WEATHER_API_KEY")
    try:

        api_key = API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
        response = requests.get(url)
    except requests.RequestException:
        return None

    try:
        weather = response.json()
        data = {
            "title": weather['weather'][0]['main'],
            "description": weather['weather'][0]['description'],
            "icon": weather['weather'][0]['icon'],
            "temp": float(weather['main']['temp']),
            "feels_like": float(weather['main']['feels_like']),
            "cloudiness": weather['clouds']['all']
        }
        return data
    except (KeyError, TypeError, ValueError):
        return None