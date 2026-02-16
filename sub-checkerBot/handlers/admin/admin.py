from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.constants import CommandText
from core.text import AdminMenu
from handlers.admin.tariffs.fsm_states import CreateTariff
from keyboards.admin_main_menu import build_main_menu

router = Router()

@router.message(Command(CommandText.ADMIN_MENU))
async def open_admin_menu(message: Message):

    await message.answer(
        text=AdminMenu.MENU,
        reply_markup=build_main_menu(),
    )

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

