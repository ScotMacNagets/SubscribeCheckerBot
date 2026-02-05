from aiogram import Router

from .users import router as users_router
from .admin import router as main_router

admin_router = Router()
admin_router.include_router(users_router)
admin_router.include_router(main_router)

__all__ = ("admin_router",)

