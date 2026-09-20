from datetime import datetime, timedelta

from .config import WORK_START_HOUR, WORK_END_HOUR, SLOT_MINUTES, DAYS_AHEAD
from .database import get_taken_slots


def get_available_dates():
    dates = []
    today = datetime.now().date()
    for i in range(DAYS_AHEAD):
        dates.append(today + timedelta(days=i))
    return dates


def generate_all_slots():
    slots = []
    start = datetime.strptime(f"{WORK_START_HOUR}:00", "%H:%M")
    end = datetime.strptime(f"{WORK_END_HOUR}:00", "%H:%M")
    current = start
    while current < end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=SLOT_MINUTES)
    return slots


async def get_free_slots(barber_id, date_str):
    all_slots = generate_all_slots()
    taken = await get_taken_slots(barber_id, date_str)
    return [s for s in all_slots if s not in taken]
