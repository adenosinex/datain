import json
import os
import sqlite3
from datetime import datetime

 
DB_FILE = r"C:\Users\xin\OneDrive\sqlite\daily_stats.db"
 

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,           -- 格式: YYYY-MM-DD HH:MM:SS
            project TEXT,
            count INTEGER,
            remark TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_record(project, time, remark="", count=None):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO stats (time, project, count, remark) VALUES (?, ?, ?, ?)",
              (time, project, count if count is not None else None, remark))
    conn.commit()
    conn.close()

def get_stats():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, time, project, count, remark FROM stats ORDER BY time DESC")
    rows = c.fetchall()
    conn.close()
    stats = []
    for id, time, project, count, remark in rows:
        stats.append({
            "id": id,
            "date": time[:10],
            "time": time[11:],
            "project": project,
            "count": count if count is not None else "",
            "remark": remark
        })
    return stats