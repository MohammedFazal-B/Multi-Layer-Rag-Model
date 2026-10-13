import sqlite3
import time
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "firewall_analytics.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            prompt TEXT,
            status TEXT,
            reason TEXT,
            score REAL,
            latency_ms REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_request(prompt, status, reason, score, latency_ms):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (timestamp, prompt, status, reason, score, latency_ms)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.utcnow().isoformat(), prompt, status, str(reason) if reason else "", score, latency_ms))
    conn.commit()
    conn.close()

def get_analytics_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total requests
    cursor.execute('SELECT COUNT(*) FROM requests')
    total = cursor.fetchone()[0]
    
    # Blocked requests
    cursor.execute('SELECT COUNT(*) FROM requests WHERE status = "BLOCK"')
    blocked = cursor.fetchone()[0]
    
    # Allowed requests
    cursor.execute('SELECT COUNT(*) FROM requests WHERE status = "ALLOW"')
    allowed = cursor.fetchone()[0]
    
    # Average latency
    cursor.execute('SELECT AVG(latency_ms) FROM requests')
    avg_latency = cursor.fetchone()[0] or 0.0
    
    # Top attack categories
    cursor.execute('''
        SELECT reason, COUNT(*) as count 
        FROM requests 
        WHERE status = "BLOCK" AND reason != ""
        GROUP BY reason 
        ORDER BY count DESC 
        LIMIT 5
    ''')
    top_categories = [{"category": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "total_requests": total,
        "blocked_requests": blocked,
        "allowed_requests": allowed,
        "average_latency_ms": round(avg_latency, 2),
        "top_attack_categories": top_categories
    }

# Initialize DB on import
init_db()
