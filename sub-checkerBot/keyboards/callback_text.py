from pydantic import BaseModel

class BackText:
    back: str = "back"

class PaymentText:
    confirm_pay: str = "confirm payment"
    cancel_pay: str = "cancel payment"

class StartText:
    buy_sub: str = "buy_subscription"

payment = PaymentText()
start = StartText()
back = BackText()