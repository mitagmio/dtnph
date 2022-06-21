start_created = "Sup, {first_name}!"
start_not_created = "Welcome back, {first_name}!"
unlock_secret_room = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "<b>Users</b>: {user_count}\n" \
           "<b>24h active</b>: {active_24}"
github_button_text = "GitHub"
secret_level_button_text = "Secret level🗝"
start_button_text = "🎉 Старт"

START_USER = """
Привет, @{username}{text}
Этот Бот .... 

<i>Мы всегда рады новым людям в команде. Если у вас есть идеи, как вы можете помочь развитию сообщества, пишите!</i>

Твой Telegram id: {tgid}"""
NOT_USER_NAME = """Привет!
{text}Мы не обслуживаем пользователей без username.
Пожалуйста открой настройки профиля и заполни свой уникальный username. ☺️

Твой Telegram id: {tgid}"""

NOT_EMAIL_NAME = """Привет!
{text}Введи пожалуйста email.

Почта потребуется для Академии и отправки полезных уведомлений. ☺️

Твой Telegram id: {tgid}"""

MENU = """
<b>ТЕКСТ МЕНЮ</b>
"""

HELP = """
<b>ПОМОЩЬ</b>
        
"""

ADMIN_MENU_TEXT = """📝 Администрирование:
выбери необходимый пункт для дальнейших действий

<code>{}</code>
"""

WALLET = """
📨 Почта: {email}

💵 Баланс: {balance} USDT

"""

WALLET_SUMM = """
На какую сумму в USDT ты хочешь пополнить?

введи сумму цифрой, например 10.6 
"""

WALLET_ADR = """
Пополни адрес кошелька TRC20 

<code>TYXmiSD7KoLmFyWoPauM2MpXfpS3Z1fsCq</code>

на уникальную сумму {summ_float} это позволит зачислить платеж в твой кошелек в боте.

Внимание! Отправляйте точную сумму до центов иначе ваш платеж может быть не распознан.
После зачисления платежа тебе придет уведомление
"""