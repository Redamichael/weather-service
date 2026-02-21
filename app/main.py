from fastapi import FastAPI
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