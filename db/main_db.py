import sqlite3
from datetime import datetime

DB_PATH = 'db/tasks.db'

def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                date_added TEXT NOT NULL,
                task_status INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def insert_task(description):
    date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (description, date_added, task_status) VALUES (?, ?, ?)', (description, date_added, 0))
        conn.commit()
        return cursor.lastrowid

def fetch_tasks(sort_by_creation_date=True, sort_by_completion_status=False, filter_in_progress=False):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        order_by_clause = "ORDER BY date_added DESC" if sort_by_creation_date else "ORDER BY date_added ASC"
        if sort_by_completion_status:
            order_by_clause = "ORDER BY task_status ASC, date_added DESC" if sort_by_creation_date else "ORDER BY task_status ASC, date_added ASC"
        
        where_clause = "WHERE task_status = 2" if filter_in_progress else ""
        
        cursor.execute(f'SELECT id, description, date_added, task_status FROM tasks {where_clause} {order_by_clause}')
        return cursor.fetchall()

def modify_task(task_id, new_description):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET description = ? WHERE id = ?', (new_description, task_id))
        conn.commit()

def update_task_status(task_id, new_status):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET task_status = ? WHERE id = ?', (int(new_status), task_id))
        conn.commit()

def clear_completed_tasks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE task_status = 1')
        conn.commit()
