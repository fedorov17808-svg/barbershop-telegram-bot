from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .config import SERVICES, BARBERS
from .services import get_available_dates


def services_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for s in SERVICES:
        builder.button(text=f"{s['title']} — {s['price']}₽", callback_data=f"service:{s['id']}")
    builder.adjust(1)
    return builder.as_markup()


def barbers_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in BARBERS:
        builder.button(text=b["name"], callback_data=f"barber:{b['id']}")
    builder.adjust(2)
    return builder.as_markup()


def dates_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for d in get_available_dates():
        builder.button(text=d.strftime("%d.%m (%a)"), callback_data=f"date:{d.isoformat()}")
    builder.adjust(2)
    return builder.as_markup()


def slots_keyboard(slots) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for slot in slots:
        builder.button(text=slot, callback_data=f"time:{slot}")
    builder.adjust(4)
    return builder.as_markup()


def confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="confirm")
    builder.button(text="❌ Отменить", callback_data="cancel")
    builder.adjust(2)
    return builder.as_markup()
