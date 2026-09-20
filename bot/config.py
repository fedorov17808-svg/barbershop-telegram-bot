import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

WORK_START_HOUR = 10
WORK_END_HOUR = 20
SLOT_MINUTES = 30
DAYS_AHEAD = 7

SERVICES = [
    {"id": "haircut", "title": "Стрижка", "price": 1200, "duration_min": 40},
    {"id": "beard", "title": "Стрижка бороды", "price": 700, "duration_min": 20},
    {"id": "combo", "title": "Стрижка + борода", "price": 1700, "duration_min": 60},
    {"id": "kids", "title": "Детская стрижка", "price": 900, "duration_min": 30},
]

BARBERS = [
    {"id": 1, "name": "Алексей"},
    {"id": 2, "name": "Дмитрий"},
    {"id": 3, "name": "Марат"},
]
