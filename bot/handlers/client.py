from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from ..config import SERVICES, BARBERS
from ..database import cancel_booking, create_booking, get_user_bookings
from ..keyboards import (
    barbers_keyboard,
    confirm_keyboard,
    dates_keyboard,
    services_keyboard,
    slots_keyboard,
)
from ..services import get_free_slots

router = Router()


class Booking(StatesGroup):
    choosing_service = State()
    choosing_barber = State()
    choosing_date = State()
    choosing_time = State()
    confirming = State()


def find_service(service_id):
    return next(s for s in SERVICES if s["id"] == service_id)


def find_barber(barber_id):
    return next(b for b in BARBERS if b["id"] == barber_id)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💈 Добро пожаловать в барбершоп!\n\n"
        "Я помогу записаться на стрижку за 30 секунд.\n"
        "Выберите услугу:",
        reply_markup=services_keyboard(),
    )
    await state.set_state(Booking.choosing_service)


@router.callback_query(Booking.choosing_service, F.data.startswith("service:"))
async def choose_service(callback: CallbackQuery, state: FSMContext):
    service = find_service(callback.data.split(":", 1)[1])
    await state.update_data(service=service)
    await callback.message.edit_text(
        f"Услуга: {service['title']} ({service['price']}₽, {service['duration_min']} мин)\n\n"
        "Выберите мастера:",
        reply_markup=barbers_keyboard(),
    )
    await state.set_state(Booking.choosing_barber)
    await callback.answer()


@router.callback_query(Booking.choosing_barber, F.data.startswith("barber:"))
async def choose_barber(callback: CallbackQuery, state: FSMContext):
    barber = find_barber(int(callback.data.split(":", 1)[1]))
    await state.update_data(barber=barber)
    await callback.message.edit_text(
        f"Мастер: {barber['name']}\n\nВыберите дату:",
        reply_markup=dates_keyboard(),
    )
    await state.set_state(Booking.choosing_date)
    await callback.answer()


@router.callback_query(Booking.choosing_date, F.data.startswith("date:"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.split(":", 1)[1]
    data = await state.get_data()
    free_slots = await get_free_slots(data["barber"]["id"], date_str)
    if not free_slots:
        await callback.answer("На эту дату у мастера всё занято, выберите другую 🙁", show_alert=True)
        return
    await state.update_data(date=date_str)
    await callback.message.edit_text(
        f"Дата: {date_str}\n\nВыберите время:",
        reply_markup=slots_keyboard(free_slots),
    )
    await state.set_state(Booking.choosing_time)
    await callback.answer()


@router.callback_query(Booking.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext):
    time_str = callback.data.split(":", 1)[1]
    await state.update_data(time=time_str)
    data = await state.get_data()
    text = (
        "📋 Проверьте запись:\n\n"
        f"Услуга: {data['service']['title']} — {data['service']['price']}₽\n"
        f"Мастер: {data['barber']['name']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {time_str}\n"
    )
    await callback.message.edit_text(text, reply_markup=confirm_keyboard())
    await state.set_state(Booking.confirming)
    await callback.answer()


@router.callback_query(Booking.confirming, F.data == "confirm")
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    booking_id = await create_booking(
        user_id=callback.from_user.id,
        user_name=callback.from_user.full_name,
        service=data["service"],
        barber=data["barber"],
        date=data["date"],
        time=data["time"],
    )
    await callback.message.edit_text(
        f"✅ Запись #{booking_id} подтверждена!\n\n"
        f"{data['service']['title']} у мастера {data['barber']['name']}\n"
        f"{data['date']} в {data['time']}\n\n"
        "Ждём вас! Посмотреть свои записи — /my_bookings"
    )
    await state.clear()
    await callback.answer()


@router.callback_query(Booking.confirming, F.data == "cancel")
async def cancel_flow(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Запись отменена. Чтобы начать заново — /start")
    await callback.answer()


@router.message(Command("my_bookings"))
async def my_bookings(message: Message):
    bookings = await get_user_bookings(message.from_user.id)
    if not bookings:
        await message.answer("У вас пока нет активных записей. Нажмите /start чтобы записаться.")
        return
    lines = ["📅 Ваши записи:\n"]
    for booking_id, service_title, barber_name, date, time, status in bookings:
        lines.append(f"#{booking_id} · {service_title} · {barber_name} · {date} {time}")
    lines.append("\nОтменить запись: /cancel <номер>")
    await message.answer("\n".join(lines))


@router.message(Command("cancel"))
async def cancel_cmd(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /cancel <номер записи>, например /cancel 5")
        return
    await cancel_booking(int(parts[1]), message.from_user.id)
    await message.answer("Запись отменена.")
