import requests
from .database import get_connection
from .alerts import send_failure_alert
from .config import WEATHER_API_KEY

def fetch_weather(city="Addis Ababa"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def transform_weather(api_data):
    return {
        "city": api_data["name"],
        "temperature": api_data["main"]["temp"],
        "humidity": api_data["main"]["humidity"],
        "weather": api_data["weather"][0]["description"],
    }

def insert_weather(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weather_data (city, temperature, humidity, weather)
        VALUES (%s, %s, %s, %s)
    """, (
        data["city"],
        data["temperature"],
        data["humidity"],
        data["weather"],
    ))

    conn.commit()
    cur.close()
    conn.close()

def run_pipeline():
    raw = fetch_weather()
    structured = transform_weather(raw)
    insert_weather(structured)

def safe_run():
    try:
        run_pipeline()
        return {"status": "success"}
    except Exception as e:
        send_failure_alert(str(e))
        raise
