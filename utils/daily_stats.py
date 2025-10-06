import json
import os
import sqlite3
from datetime import datetime
import time

 
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
last_add=0
def add_record(project, addtime, remark="", count=None):
    global last_add
    if last_add==addtime:
        return
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    r=c.execute("SELECT time FROM stats WHERE remark='auto' order by id desc" ).fetchone()
    if r:
        # 重复auto项目，10秒内不重复添加
        timstrap=datetime.strptime(r[0],'%Y-%m-%d %H:%M:%S')
        time_new=datetime.strptime( addtime,'%Y-%m-%d %H:%M:%S' )
        td=time_new.timestamp()-timstrap.timestamp()
        if  td<10:
            conn.close()
            return
    c.execute("INSERT INTO stats (time, project, count, remark) VALUES (?, ?, ?, ?)",
              (addtime, project, count if count is not None else None, remark))
    conn.commit()
    conn.close()
# add_record("test_project", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "auto" )

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

def delete_record(record_id):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM stats WHERE id=?", (record_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    return affected > 0


if __name__ == "__main__":
    init_db()
   
    stats = get_stats()
 