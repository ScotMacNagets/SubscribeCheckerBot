from datetime import date


def self_check_text(subscription_end: date | None) -> str:
    if subscription_end:
        days_left = (subscription_end - date.today()).days
        if days_left < 0:
            return (
                f"⚠️ Ваша подписка закончилась {subscription_end.strftime('%d.%m.%Y')}.\n"
                f"Вы можете продлить подписку, чтобы снова получить доступ к закрытому каналу."
            )
        if days_left < 30 :
            return (
                f"📅 Ваша подписка активна до <b>{subscription_end.strftime('%d.%m.%Y')}</b>.\n"
            )
        return (
            f"📅 Ваша подписка активна до <b>{subscription_end.strftime('%d.%m.%Y')}</b>.\n"
            f"Осталось дней: <b>{days_left}</b>."
        )
    else:
        return (
            "⚠️ У Вас нет активной подписки.\n"
            "Вы можете оформить её, чтобы получить доступ к закрытому каналу."
        )