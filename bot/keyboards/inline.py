from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌤 Погода", callback_data="weather"),
            InlineKeyboardButton(text="📰 Новости", callback_data="news"),
        ],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    ])


def settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏙 Изменить город", callback_data="set_city")],
        [InlineKeyboardButton(text="⏰ Изменить время уведомления", callback_data="set_time")],
        [InlineKeyboardButton(text="🔔 Вкл/Выкл уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
    ])
