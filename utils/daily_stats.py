import json
import os
import sqlite3
from datetime import datetime

DATA_FILE = "data/daily_stats.json"
DB_FILE = "data/daily_stats.db"

def load_stats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f)

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
    c.execute("SELECT time, project, count, remark FROM stats ORDER BY time DESC")
    rows = c.fetchall()
    conn.close()
    stats = []
    for time, project, count, remark in rows:
        stats.append({
            "date": time[:10],      # 提取日期
            "time": time[11:],      # 提取时分秒
            "project": project,
            "count": count if count is not None else "",
            "remark": remark
        })
    return stats