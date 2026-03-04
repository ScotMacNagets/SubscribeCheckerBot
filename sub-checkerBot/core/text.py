
#HANDLERS:


#Start
class StartHandler:
    START=(
        "Приветствую! 👋 \n"
        "Этот бот поможет Вам подключить подписку и сразу получить доступ к закрытому каналу."
    )

#SubBuy
class TariffHandler:
    TARIFF = "Отлично! Теперь выбери тариф😊"
    TARIFF_SELECTED=(
    "📌Вы выбрали тариф «{title}».\n\n"
    "Подтвердить оплату?🤔"
    )

class InvoiceHandler:
    INVOICE_LABEL="Подписка {tariff}"
    INVOICE_TITLE="Подписка"
    CURRENCY="RUB"

class SuccessfulPayment:
    SUCCESSFUL_INVITE=(
        "✅ Оплата прошла успешно!\n\n"
        "📋 Тариф: {title}\n"
        "📅 Подписка активна до {end_date}\n\n"
        "🎉 Доступ к закрытому каналу активирован!"
    )
    UNSUCCESSFUL_INVITE = (
        "✅ Оплата прошла успешно!\n\n"
        "📋 Тариф: {title}\n"
        "📅 Подписка активна до {end_date}\n\n"
        "⚠️ Не удалось автоматически добавить вас в канал. "
        "Обратитесь к <a href='https://t.me/{admin_username}'>администратору</a> " 
        "для получения доступа."
    )
    INVITE_LINK="\n\n🔗 Ссылка на канал: {invite_link}\n(действует 24 часа)"
    ACTIVATE_ERROR=(
        "❌ Произошла ошибка при активации подписки. "
        "Ваш платеж зарегистрирован. Обратитесь к <a href='https://t.me/{admin_username}'>поддержке.</a>"
    )

#CheckSub
class CheckSubServices:
    THREE_DAYS_LEFT="⏰ Ваша подписка заканчивается через 3 дня! Продлите её, чтобы не потерять доступ."
    ONE_DAY_LEFT="⚠️ Ваша подписка заканчивается завтра! Продлите её сейчас."
    SUBSCRIBE_EXPIRED="❌ Ваша подписка истекла сегодня. Доступ к каналу будет закрыт."

class CheckSubHandlers:
    SUBSCRIPTION_EXPIRED=(
        "⚠️ Ваша подписка закончилась {end_date}.\n"
        "Вы можете продлить подписку, чтобы снова получить доступ к закрытому каналу."
    )
    SUBSCRIPTION_ACTIVE_UNTIL="📅 Ваша подписка активна до <b>{end_date}</b>.\n"
    DAYS_LEFT="Осталось дней: <b>{days_left}</b>."
    DONT_HAVE_SUBSCRIPTION=(
        "⚠️ У Вас нет активной подписки.\n"
        "Вы можете оформить её, чтобы получить доступ к закрытому каналу."
    )

#ADMIN

#Main
class AdminMenu:
    MENU="🔧 Добро пожаловь в меню администратора\n\n Выберете, что хотите сделать:"
    ACCESS_RESTRICTED="⛔ У вас нет доступа к админ-меню"
    OPEN_ADMIN_MENU_ERROR="😥 Ошибка при открытии меню. Попробуйте позже"

#Users
class AdminUsersMenu:
    USER_MANAGE_MENU="👥 Меню управления пользователями"

class AdminUserAction:
    ENTER_USERNAME="Введите ник пользователя, которого нужно найти."
    INCORRECT_DATA="❌ Некорректные данные."
    USER_NOT_FOUND="❌ Ошибка системы, не удалось найти пользователя"
    EXTEND_FAILED="❌ Ошибка продления, попробуйте позже"
    INCORRECT_DATA_FORMAT="❌ Некорректный формат даты. Используйте ДД.ММ.ГГГГ, например 25.12.2026."
    PAST_DATE="❌ Дата не может быть в прошлом. Введите корректную дату."
    CANNOT_IDENTIFY_USER="❌ Не удалось определить пользователя. Попробуйте снова через меню админа."
    FAILED_TO_EXTEND_SUB="❌ Не удалось продлить подписку"
    SET_NEW_DATE=(
        "Введите новую дату окончания подписки для пользователя {username} "
        "в формате ДД.ММ.ГГГГ.\n"
        "Например: 25.12.2026\n"
    )
    USER_NOT_FOUND_OR_DELETED= "Пользователь не найден или уже удалён."


class AdminUsersHelpersText:
    FORMAT_SHORT= "🟢 активна, до {date} ({days_left} дн.)"
    SHORT_NO_SUB="❌ нет подписки"
    FORMAT_DETAIL=(
        "👤 <b>Пользователь</b>\n\n"
        "ID: <code>{id}</code>\n"
        "Username: @{username}\n"
        "Создан: {date}"
    )
    USER_NOT_FOUND="❌ Пользователь не найден"
    USER_SUCCESSFULLY_DELETED="✅ Пользователь успешно удален"

    STATUS_ACTIVE="🟢 активна"
    STATUS_EXPIRED="🔴 истекла"

    SUB_DESC="Подписка: {status}, до {date} (дней: {days_left})"

    USER_GOT_NO_SUB="❌ Подписка: отсутствует"


#Tariff

class AdminTariffMenu:
    TARIFF_MENU= "📈 Меню управления тарифами"
    AFTER_DELETING= "Тариф удалён.\n\n 📈 Меню управления тарифами:"


class AdminAllTariffText:
    TARIFF_DETAILED_LINE=(
        "📦 <b>Тариф</b>\n"
        "🗿 Название: {title}\n"
        "📅 Срок: {days}\n"
        "💵 Цена: {price}₽\n"
        "🔥 Горячий: {hot}\n"
        "🟢 Активен: {is_active}"
    )

    #CreateTariff
    START_MESSAGE=(
        "🎨 Давайте приступим к созданию нового тарифа\n\n"
        "Для начала введите название нового тарифа:"
    )
    SET_TARIFF_PRICE="💵 Теперь укажите цену тарифа"
    SET_DURATION_IN_DAYS="📅 Теперь укажите длительность тарифа в днях"

    CONFIRMING_TEXT=(
        "📄 Проверьте данные\n\n"
        "🗿 Название: {title}\n"
        "💵 Цена: {price}₽\n"
        "📅 Срок: {days} дней\n"
    )

    CREATING_ERROR="❌ Ошибка при создании тарифа, попробуйте позже"
    TARIFF_ALREADY_EXISTS="❌Ошибка. Такой тариф уже существует"

#Broadcast

class AdminBroadcastText:
    BROADCAST_MENU="📢 Меню рассылки"
    SEND_MESSAGE="✍️ Отправьте сообщение для рассылки"
    SEND_PHOTO="Теперь прикрепите картинку к рассылке😊"

    CONFIRM_MESSAGE="🤔 Вы уверены, что хотите отправить сообщение в таком виде?"

    BROADCAST_SENT= "✅ Рассылка завершена"
    BROADCAST_CANCELED="❌ Рассылка отменена"


#BUTTONS:

class GeneralButtons:
    BACK_BUTTON="⬅ Назад"
    BACK_TO_ADMIN="⬅ Вернуться в админ меню"

#start_keyboard
class StartKeyboard:
    BUY_SUBSCRIPTION="✨Приобрести подписку✨"
    CHECK_SUBSCRIPTION="🔎📂Посмотреть текущую подписку🔎📂"

#renewkeyboard
class RenewKeyboard:
    BUY_SUBSCRIPTION="💳 Приобрести подписку"

#paymentkeyboard
class PaymentKeyboard:
    PAY="💳 Оплатить"
    CANCEL_PAYMENT="⛔ Отменить оплату"

#admin_users_keyboard
class AdminUsersKeyboard:
    EXTEND_DAYS="➕ +{days} дней"
    SET_THE_DATE="📅 Установить дату"
    CANCEL_SUB="✂ Отменить подписку"
    DELETE_USER="🗑 Удалить пользователя"
    USERNAME_SEARCH="📂🔍 Поиск по нику"

#admin_tariffs_keyboard

class AdminTariffKeyboard:
    #List
    ACTIVE_STATUS="🟢"
    NON_ACTIVE_STATUS="⚪️"
    TARIFF_LIST_TEXT="{status} {title} — {price}₽"

    #Detailed_keyboard
    ACTIVE="✅ Активен"
    NON_ACTIVE="🚫 Неактивен"

    HOT="🔥 Горячий"
    NOT_HOT="💤 Обычный"

    DELETE="🗑 Удалить"
    BACK_TO_THE_LIST="⬅ К списку тарифов"

    #Create

    START_CREATING="✏ Создать новый тариф"
    #Confirm
    CONFIRM="✅ Подтвердить"
    CANCEL="⛔ Отменить"

    CONFIRMED="✅ Тариф успешно создан"
    CANCELED="⛔ Создание тарифа отменено"


#admin_broadcast_keyboard

class AdminBroadcastKeyboard:
    START_BROADCAST="📢 Сделать рассылку"

    # Confirm
    CONFIRM = "✅ Подтвердить"
    CANCEL = "⛔ Отменить"

    WRITE_TEXT="✍️ Ввести текст"


#REDIS

class RedisAnswers:
    TOO_MANY_REQUESTS="⏳ Слишком много запросов. Попробуйте позже."




