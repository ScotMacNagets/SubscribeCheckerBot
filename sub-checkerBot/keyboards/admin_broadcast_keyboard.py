from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks.admin_broadcast_callbackdata import BroadcastCB
from callbacks.admin_callback_text import AdminBroadcastActions
from core.text import AdminBroadcastKeyboard


def build_broadcast_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminBroadcastKeyboard.WRITE_TEXT,
        callback_data=BroadcastCB(action=AdminBroadcastActions.START).pack()
    )

    builder.button(
        text=AdminBroadcastKeyboard.CANCEL,
        callback_data=BroadcastCB(action=AdminBroadcastActions.CANCEL).pack()
    )

    builder.adjust(1)
    return builder.as_markup()

def builder_confirm_broadcast_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=AdminBroadcastKeyboard.CONFIRM,
        callback_data=BroadcastCB(action=AdminBroadcastActions.CONFIRM).pack()
    )
    builder.button(
        text=AdminBroadcastKeyboard.CANCEL,
        callback_data=BroadcastCB(action=AdminBroadcastActions.CANCEL).pack()
    )

    builder.adjust(2)
    return builder.as_markup()
