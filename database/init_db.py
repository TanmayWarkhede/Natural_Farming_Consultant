"""
Optional lightweight database initialisation.
Creates SQLite tables for session logging (not required for core functionality).
"""
import os
import sqlite3

DB_PATH = os.path.join("database", "farming_logs.db")


def init_database():
    """Create database tables if they don't exist."""
    try:
        os.makedirs("database", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disease_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                image_name TEXT,
                detected_disease TEXT,
                severity TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                humidity REAL,
                rainfall REAL,
                risks TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database init warning: {e}")
        return False


def log_disease_analysis(image_name: str, disease: str, severity: str):
    """Log a disease detection event."""
    try:
        import datetime
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO disease_logs (timestamp, image_name, detected_disease, severity) VALUES (?,?,?,?)",
            (datetime.datetime.now().isoformat(), image_name, disease, severity),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # Logging failure should never crash the app


def log_weather_query(city: str, temp: float, humidity: float, rainfall: float, risks: str):
    """Log a weather query event."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO weather_logs (city, temperature, humidity, rainfall, risks) VALUES (?,?,?,?,?)",
            (city, temp, humidity, rainfall, risks),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


if __name__ == "__main__":
    if init_database():
        print("✅ Database initialised successfully.")
    else:
        print("⚠️ Database initialisation failed (non-critical).")
