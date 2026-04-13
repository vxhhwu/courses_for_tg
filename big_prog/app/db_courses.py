import aiosqlite
from datetime import datetime

DB_PATH = "database_courses.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def save_new_course(id: int, title: str, description: str, category: str, price: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO courses (id, title, description, category, price, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, title, description, category, price, datetime.now()))
        await db.commit()

async def get_courses():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT id, title, description, category, price FROM courses') as cursor:  
            rows = await cursor.fetchall()
            return rows
        
async def get_courses_by_category(category: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT id, title FROM courses WHERE category = ?', (category,)) as cursor:
            rows = await cursor.fetchall()
            return rows
        
async def get_course_by_id(id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT title, description, category, price FROM courses WHERE id = ?', (id,)) as cursor:
            rows = await cursor.fetchone()
            return rows
        
async def del_courses(id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('DELETE FROM courses WHERE id = ?', (id,))
        await db.commit()
        return cursor.rowcount > 0