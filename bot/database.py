import aiosqlite
from datetime import datetime

DB_PATH = "barbershop.db"

CREATE_BOOKINGS_TABLE = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_name TEXT,
    service_id TEXT NOT NULL,
    service_title TEXT NOT NULL,
    barber_id INTEGER NOT NULL,
    barber_name TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'confirmed',
    created_at TEXT NOT NULL
)
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_BOOKINGS_TABLE)
        await db.commit()


async def create_booking(user_id, user_name, service, barber, date, time):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO bookings
               (user_id, user_name, service_id, service_title, barber_id, barber_name, date, time, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, user_name, service["id"], service["title"], barber["id"], barber["name"],
             date, time, datetime.now().isoformat())
        )
        await db.commit()
        return cursor.lastrowid


async def get_taken_slots(barber_id, date):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT time FROM bookings WHERE barber_id = ? AND date = ? AND status = 'confirmed'",
            (barber_id, date)
        )
        rows = await cursor.fetchall()
        return {row[0] for row in rows}


async def get_user_bookings(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """SELECT id, service_title, barber_name, date, time, status
               FROM bookings WHERE user_id = ? AND status = 'confirmed'
               ORDER BY date, time""",
            (user_id,)
        )
        return await cursor.fetchall()


async def cancel_booking(booking_id, user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE id = ? AND user_id = ?",
            (booking_id, user_id)
        )
        await db.commit()


async def get_bookings_for_date(date):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """SELECT user_name, service_title, barber_name, time
               FROM bookings WHERE date = ? AND status = 'confirmed'
               ORDER BY time""",
            (date,)
        )
        return await cursor.fetchall()


async def get_upcoming_bookings():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """SELECT user_name, service_title, barber_name, date, time
               FROM bookings WHERE status = 'confirmed'
               ORDER BY date, time"""
        )
        return await cursor.fetchall()
