from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..config import ADMIN_ID
from ..database import get_bookings_for_date, get_upcoming_bookings

router = Router()


def is_admin(user_id: int) -> bool:
    return ADMIN_ID != 0 and user_id == ADMIN_ID


@router.message(Command("today"))
async def today_bookings(message: Message):
    if not is_admin(message.from_user.id):
        return
    today_str = date.today().isoformat()
    rows = await get_bookings_for_date(today_str)
    if not rows:
        await message.answer("Сегодня записей нет.")
        return
    lines = [f"📋 Записи на сегодня ({today_str}):\n"]
    for user_name, service_title, barber_name, time in rows:
        lines.append(f"{time} · {user_name} · {service_title} · {barber_name}")
    await message.answer("\n".join(lines))


@router.message(Command("all_bookings"))
async def all_bookings(message: Message):
    if not is_admin(message.from_user.id):
        return
    rows = await get_upcoming_bookings()
    if not rows:
        await message.answer("Активных записей нет.")
        return
    lines = ["📋 Все предстоящие записи:\n"]
    for user_name, service_title, barber_name, d, time in rows:
        lines.append(f"{d} {time} · {user_name} · {service_title} · {barber_name}")
    await message.answer("\n".join(lines))
