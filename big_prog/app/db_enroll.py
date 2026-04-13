import aiosqlite
from datetime import datetime

DB_PATH = 'database_mycourses.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS my_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                price INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, course_id)
            )
        ''')
        await db.commit()

async def add_my_course(user_id: int, course_id: int, title: str, description: str, category: str, price: int):
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute('''
                INSERT INTO my_courses (user_id, course_id, title, description, category, price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, course_id, title, description, category, price))
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False

async def get_my_courses(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT course_id, title, description, category, price FROM my_courses WHERE user_id = ?', (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def is_already_enrolled(user_id: int, course_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT 1 FROM my_courses WHERE user_id = ? AND course_id = ?', (user_id, course_id)) as cursor:
            return await cursor.fetchone() is not None
        
async def del_my_course(user_id: int, course_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('DELETE FROM my_courses WHERE user_id = ? AND course_id = ?', (user_id, course_id))
        await db.commit()
        return cursor.rowcount > 0