from flask import Flask, request, render_template
import sqlite3
import os

DB_NAME = 'inspections.db'
PAGE_SIZE = 10

app = Flask(__name__)

# Убедимся, что папка templates существует
if not os.path.exists('templates'):
    os.makedirs('templates')


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    q = request.args.get('q', '').strip()
    offset = (page - 1) * PAGE_SIZE
    conn = get_db_connection()
    cur = conn.cursor()
    if q:
        like_q = f"%{q}%"
        cur.execute(f'SELECT COUNT(*) FROM inspections WHERE entity_name LIKE ? COLLATE NOCASE', (like_q,))
        total = cur.fetchone()[0]
        total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
        cur.execute(f'SELECT * FROM inspections WHERE entity_name LIKE ? COLLATE NOCASE ORDER BY id LIMIT ? OFFSET ?', (like_q, PAGE_SIZE, offset))
    else:
        cur.execute(f'SELECT COUNT(*) FROM inspections')
        total = cur.fetchone()[0]
        total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
        cur.execute(f'SELECT * FROM inspections ORDER BY id LIMIT ? OFFSET ?', (PAGE_SIZE, offset))
    rows = cur.fetchall()
    conn.close()
    return render_template('index.html', rows=rows, page=page, total_pages=total_pages, request=request)

if __name__ == '__main__':
    app.run(debug=True) 