from .tariffs import router as tariffs_router
from .create_tariff import router as create_tariffs_router

__all__ = (
    "tariffs_router",
    "create_tariffs_router"
)