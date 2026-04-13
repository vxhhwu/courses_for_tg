import aiosqlite
from datetime import datetime

DB_PATH = "database_users.db"

async def init_db():
    """Создаёт таблицу users при первом запуске."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def save_user(user_id: int, first_name: str, last_name: str, age: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (user_id, first_name, last_name, age, registered_at)
            VALUES (?, ?, ?, ?, COALESCE((SELECT registered_at FROM users WHERE user_id = ?), ?))
        ''', (user_id, first_name, last_name, age, user_id, datetime.now()))
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT first_name, last_name, age FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"first_name": row[0], "last_name": row[1], "age": row[2]}
            return None
        
async def del_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        await db.commit()
        return cursor.rowcount > 0
    
async def user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row is not None