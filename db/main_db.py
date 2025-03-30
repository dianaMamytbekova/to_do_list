import sqlite3
from datetime import datetime

DB_PATH = 'db/todo.db'


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status INTEGER DEFAULT 0
            )
        ''')
        conn.commit()


def add_task_db(task_text):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (text, created_at, status) VALUES (?, ?, ?)', (task_text, created_at, 0))
        conn.commit()
        return cursor.lastrowid


def get_tasks(sort_by_date=True, sort_by_status=False):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        order_clause = "ORDER BY created_at DESC" if sort_by_date else "ORDER BY created_at ASC"
        if sort_by_status:
            order_clause = "ORDER BY status ASC, created_at DESC" if sort_by_date else "ORDER BY status ASC, created_at ASC"
        
        cursor.execute(f'SELECT id, text, created_at, status FROM tasks {order_clause}')
        return cursor.fetchall()


def update_task_db(task_id, new_text):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET text = ? WHERE id = ?', (new_text, task_id))
        conn.commit()


def update_task_status(task_id, status):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (int(status), task_id))
        conn.commit()
