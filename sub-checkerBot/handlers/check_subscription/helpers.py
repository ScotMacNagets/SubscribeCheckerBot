from datetime import datetime, timezone

from core.text import CheckSubHandlers


def self_check_text(subscription_end: datetime | None) -> str:
    if subscription_end:
        days_left = (subscription_end - datetime.now(timezone.utc)).days
        end_date = subscription_end.strftime('%d.%m.%Y')
        if days_left < 0:
            return (
                CheckSubHandlers.SUBSCRIPTION_EXPIRED.format(end_date=end_date)
            )
        if days_left < 30 :
            return (
                CheckSubHandlers.SUBSCRIPTION_ACTIVE_UNTIL.format(
                    end_date=end_date
                )+
                CheckSubHandlers.DAYS_LEFT.format(
                    days_left=days_left
                )
            )
        return (
            CheckSubHandlers.SUBSCRIPTION_ACTIVE_UNTIL.format(end_date=end_date)
        )
    else:
        return (
            CheckSubHandlers.DONT_HAVE_SUBSCRIPTION
        )