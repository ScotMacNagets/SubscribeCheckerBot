from core.models.tariff import Tariff


def format_tariff_button(tariff: Tariff) -> str :
    if tariff.hot:
        return f"{tariff.emoji} {tariff.title} — {tariff.price}₽ {tariff.emoji}"
    return f"{tariff.title} — {tariff.price}₽"