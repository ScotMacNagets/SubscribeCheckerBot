from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.constants import CommandText
from handlers.admin.helpers import open_admin_menu_helper

router = Router()

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):

    await open_admin_menu_helper(message=message)

@router.message(Command(CommandText.CREATE_TARIFF))
async def stat_create_tariff(
        message: Message,
        state: FSMContext,
):
    await state.set_state(CreateTariff.title)
    await message.answer(
        text=(
            "Давайте приступим к созданию нового тарифа\n\n"
            "Для начала введите название нового тарифа:"
        )
    )

