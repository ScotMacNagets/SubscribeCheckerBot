from pydantic import BaseModel


class Tariff(BaseModel):
    id: str
    title: str
    days: int
    price: int
    payload: str
    hot: bool = False
    emoji: str


TARIFFS: dict[str, Tariff]= {
    "plan_1": Tariff(
        id="plan_1",
        title="1 месяц",
        days=30,
        price=10000,
        payload="sub_1_month"
,       hot=False,
        emoji=""

    ),
    "plan_3": Tariff(
        id="plan_3",
        title="3 месяца",
        days=90,
        price=50000,
        payload="sub_3_months",
        hot=False,
        emoji=""
    ),
    "plan_6": Tariff(
        id="plan_6",
        title="6 месяцев",
        days=180,
        price=90000,
        payload="sub_6_months",
        hot=True,
        emoji="💎"
    )

}