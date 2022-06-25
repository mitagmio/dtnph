start_created = "Sup, {first_name}!"
start_not_created = "Welcome back, {first_name}!"
unlock_secret_room = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "<b>Users</b>: {user_count}\n" \
           "<b>24h active</b>: {active_24}"
github_button_text = "GitHub"
secret_level_button_text = "Secret level🗝"
start_button_text = "🎉 Старт"

START_USER = """
ℹ️ Приветствую тебя в боте P2P INVEST!{text}

Здесь ты можешь инвестировать и зарабатывать на нашей работе.
"""
NOT_USER_NAME = """ℹ️ Приветствую тебя в боте P2P INVEST!!
{text}Мы не обслуживаем пользователей без username.
Пожалуйста открой настройки профиля и заполни свой уникальный username. ☺️
"""

NOT_CHACK_IN = """ℹ️ Для начала подпишись на наш основной канал, где мы будем публиковать последние новости нашего проекта.
"""

NOT_EMAIL_NAME = """ℹ️ Приветствую тебя в боте P2P INVEST!!
{text}Введи пожалуйста email.
"""

MENU = """
ℹ️ Добро пожаловать в главное меню
"""

HELP = """
<b>ПОМОЩЬ</b>
        
"""

ADMIN_MENU_TEXT = """📝 Администрирование:
выбери необходимый пункт для дальнейших действий

<code>{}</code>
"""

WALLET = """
📱 Личный кабинет

💱 Инвестировано: {balance}$
💵 Баланс для вывода: {balance_withdrawal}$
💰 Заработано всего: {total_profit}$
"""

WALLET_SUMM = """
На какую сумму в USDT ты хочешь пополнить?

введи сумму цифрой, например 10.6 
"""

WALLET_ADDR = """
Пополни адрес кошелька TRC20 

<code>{addr}</code>

на уникальную сумму  это позволит зачислить платеж в твой кошелек в боте.

Внимание! Отправляйте точную сумму до центов иначе ваш платеж может быть не распознан.
После зачисления платежа тебе придет уведомление
"""