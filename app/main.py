from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from .database import create_table
from .pipeline import safe_run

app = FastAPI()
scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():
    create_table()

    if not scheduler.running:
        scheduler.add_job(safe_run, "interval", minutes=30)
        scheduler.start()

@app.get("/")
def root():
    return {"status": "Weather Service Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def manual_run():
    return safe_run()
from .database import get_connection

@app.get("/records")
def get_records():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM weather_data;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, city, temperature, humidity, weather, created_at
        FROM weather_data
        ORDER BY created_at DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Build HTML table
    html = """
    <html>
        <head>
            <title>Weather Records</title>
            <style>
                body { font-family: Arial; padding: 20px; background-color: #f4f4f4; }
                table { border-collapse: collapse; width: 100%; background: white; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                th { background-color: #2c3e50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h2>Weather Data Records</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>City</th>
                    <th>Temperature (°C)</th>
                    <th>Humidity (%)</th>
                    <th>Weather</th>
                    <th>Timestamp</th>
                </tr>
    """

    for row in rows:
        html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
            </tr>
        """

    html += """
            </table>
        </body>
    </html>
    """

    return html