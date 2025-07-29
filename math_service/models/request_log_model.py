# Maxim Dragos, Data Engineer

# SQLite

import sqlite3
from math_service.schemas.log_schema import LogEntry

DB_PATH = 'C:/Endava/EnDevLocal/PYCHARMproj/Dava_X/ms_API_math_comp/requests.db'
print(">>> request_log_model.py loaded!")
print(">>> DB_PATH is", DB_PATH)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                input_data TEXT NOT NULL,
                result TEXT NOT NULL,
                status_code INTEGER NOT NULL
            );
        """)
        conn.commit()


init_db()


def log_to_db(entry: LogEntry):
    print(">>>> log_to_db CALLED with", entry)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO requests_logs (operation, input_data, result, status_code)
            VALUES (?, ?, ?, ?)
        """, (
            entry.operation,
            str(entry.input_data),
            entry.result,
            entry.status_code
        ))
        conn.commit()
