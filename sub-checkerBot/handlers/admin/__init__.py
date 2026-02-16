from aiogram import Router

from .users import router as users_router
from .admin import router as main_router
from .tariffs import tariffs_router
from .tariffs import create_tariffs_router

admin_router = Router()
admin_router.include_router(users_router)
admin_router.include_router(main_router)
admin_router.include_router(tariffs_router)
admin_router.include_router(create_tariffs_router)

__all__ = ("admin_router",)

