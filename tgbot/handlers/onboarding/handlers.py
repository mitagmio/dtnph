import datetime
import time

from django.utils import timezone
from telegram import Bot, ParseMode, Update
from telegram.ext import CallbackContext
from traitlets import Float

from tgbot.handlers.onboarding import static_text, static_state
from tgbot.handlers.utils.info import extract_user_data_from_update, generate_qr
from tgbot.models import User, Invoice
from tgbot.handlers.onboarding.keyboards import *

# Отслеживаем вход в группу и назначаем рефералом в случае приглашения нового пользователя.


def status_handler_func(update: Update, context: CallbackContext):
    print('status_handler_func', update)
    # if hasattr(update, 'message') and update.message != None:
        # if update.message.chat.id == -1001793015412:
            # User.set_ref_user(update, context)

# Принимаем любой текст и проверяем состояние пользователя


def message_handler_func(update: Update, context: CallbackContext):
    print('message_handler_func', update)
    u = User.get_user(update, context)
    if update.message.chat.id != -1001793015412:
        if u.state in State_Dict:
            func_menu = State_Dict[u.state]
            func_menu(update, context)
        elif update.message.text in Menu_Dict:  # button_message проверяем текст на соответствие любой кнопке
            func_menu = Menu_Dict[update.message.text]
            func_menu(update, context)
        else:
            del_mes(update, context)


def callback_inline(update: Update, context: CallbackContext):
    # Если сообщение из чата с ботом
    # print('callback_inline', update)
    call_list = [''
                 ]
    call = update.callback_query
    if call.message:
        call_func = call.data.split(' ')
        if len(call_func) > 1:
            if call_func[0] in call_list:
                func_menu = Menu_Dict[call_func[0]]
                func_menu(update, context, call_func[1])
        else:
            func_menu = Menu_Dict[call.data]
            func_menu(update, context)
    # Если сообщение из инлайн-режима
    # elif call.inline_message_id:
    #	func_menu = Menu_Dict[call.data]
    #	func_menu(call, context)

# Удаляем записи для отображения только одной


# функция удаляющая предыдущие сообщения бота (делает эффект обновления меню при нажатии кнопки) и человека по States.S_MENU(всегда, если его статус=1)
def del_mes(update: Update, context: CallbackContext, bot_msg: bool = False):
    message = get_message_bot(update)
    try:
        context.bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    if bot_msg:
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-1)
        except:
            pass
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-2)
        except:
            pass
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-3)
        except:
            pass
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-4)
        except:
            pass
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-5)
        except:
            pass
        # time.sleep(0.1)
        try:
            context.bot.delete_message(
                message.chat.id, int(message.message_id)-6)
        except:
            pass

# Распаковываем message


def get_message_bot(update):
    if hasattr(update, 'message') and update.message != None:
        message = update.message
    if hasattr(update, 'callback_query') and update.callback_query != None:
        message = update.callback_query.message
    return message

# Проверяем является ли float


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#{'user': {'id': 1821543506, 'last_name': 'Абрамова', 'is_bot': False, 'first_name': 'Алла', 'language_code': 'ru', 'username': 'abralalalaa'}, 'status': 'left', 'until_date': None}

def check_in(update: Update, context: CallbackContext, chat_id: int|str = -1001606481866):
    message = get_message_bot(update)
    u = User.get_user(update, context)
    check_in_user = context.bot.get_chat_member(chat_id=chat_id, user_id=u.user_id)
    print(check_in_user)
    if hasattr(check_in_user, 'status') and (check_in_user.status == 'left' or check_in_user.status == 'kicked'):# 'left' 'member' 'kicked'
        u.state = static_state.S_CHECK_IN
        id = context.bot.send_message(message.chat.id, static_text.NOT_CHACK_IN, reply_markup=make_keyboard_for_check_in())  # отправляет приветствие и кнопку
        u.message_id = id.message_id
        u.save()
        return False
    return True


# Проверка на username


def check_username(update: Update, context: CallbackContext, text='\n'):
    message = get_message_bot(update)
    if not hasattr(message.chat, 'username') or message.chat.username == '' or message.chat.username == None:
        u = User.get_user(update, context)
        u.state = static_state.S_USERNAME
        id = context.bot.send_message(message.chat.id, static_text.NOT_USER_NAME.format(
            text=text, tgid=message.chat.id), reply_markup=make_keyboard_for_check_in())  # отправляет приветствие и кнопку
        u.message_id = id.message_id
        u.save()
        return False
    return True

# Проверка на email
def chenge_email(update: Update, context: CallbackContext, text='\n'):
    message = get_message_bot(update)
    u, _ = User.get_user_and_created(update, context)
    u.state = static_state.S_EMAIL
    id = context.bot.send_message(message.chat.id, static_text.NOT_EMAIL_NAME.format(
        text=text, tgid=message.chat.id), reply_markup=make_keyboard_for_check_username())  # отправляет приветствие и кнопку
    u.message_id = id.message_id
    u.save()
    del_mes(update, context, True)

def check_email(update: Update, context: CallbackContext, text='\n'):
    message = get_message_bot(update)
    u, _ = User.get_user_and_created(update, context)
    if u.email == '' or u.email == None:
        u = User.get_user(update, context)
        u.state = static_state.S_EMAIL
        id = context.bot.send_message(message.chat.id, static_text.NOT_EMAIL_NAME.format(
            text=text, tgid=message.chat.id), reply_markup=make_keyboard_for_check_username())  # отправляет приветствие и кнопку
        u.message_id = id.message_id
        u.save()
        return False
    return True

def s_email(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    message = get_message_bot(update)
    email = message.text
    try:
        u.email = email
        u.state = static_state.S_MENU
        u.save()
    except:
        del_mes(update, context, True)
        return check_email(update, context)
    cmd_wallet(update, context)
# Начало диалога


def command_start(update: Update, context: CallbackContext):
    u, _ = User.get_user_and_created(update, context)
    message = get_message_bot(update)
    # if check_in(update, context):
        # if u.state == static_state.S_ACCEPTED_ORDER:
        #     cmd_accepted_order_show(update, context)
        #     return
        # if u.state == static_state.S_USERNAME:
        #     cmd_wallet(update, context)
        #     del_mes(update, context, True)
        #     return
    text = '\n'
    u.state = static_state.S_MENU
    id = context.bot.send_message(message.chat.id, static_text.START_USER.format(
        text=text, tgid=message.chat.id), reply_markup=make_keyboard_for_start(), parse_mode="HTML")  # отправляет приветствие и кнопку
    u.message_id = id.message_id
    u.save()
    del_mes(update, context, True)

    # if created:
    #     text = static_text.start_created.format(first_name=u.first_name)
    # else:
    #     text = static_text.start_not_created.format(first_name=u.first_name)

    # update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())


# Меню


def cmd_menu(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    message = get_message_bot(update)
    if check_in(update, context):
        # помечаем состояние пользователя.
        u.state = static_state.S_MENU
        id = context.bot.send_message(
            message.chat.id, static_text.MENU, reply_markup=make_keyboard_for_cmd_menu(u.is_admin), parse_mode="HTML")
        u.message_id = id.message_id
        u.save()
    del_mes(update, context, True)


# Кошелек

def cmd_wallet(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    message = get_message_bot(update)
    # помечаем состояние пользователя.
        # Если пользователь без username мы предлагаем ему заполнить свой профиль.
    # print(bot.get_chat_member(352482305))
    # if check_email(update, context):
    if check_in(update, context):
        u.state = static_state.S_MENU
        text_email = ''
        if u.email != None and u.email != '':
            text_email = '📨 Почта: '+u.email
        id = context.bot.send_photo(
            chat_id=message.chat.id, photo=open('dtb/media/photo_2022-06-23_23-23-23.jpg', 'rb'), caption=static_text.WALLET.format(balance=u.balance, balance_withdrawal=u.balance_withdrawal, total_profit=u.total_profit), reply_markup=make_keyboard_for_cmd_wallet(text_email), parse_mode="HTML")
        u.message_id = id.message_id
        u.save()
    del_mes(update, context, True)

# Кнопка пополнения USDT TRC20 

def cmd_top_up_wallet_usdt(update: Update, context: CallbackContext):
    u = User.set_user_addr(update, context)
    message = get_message_bot(update)
    # if check_username(update, context):
        # if check_email(update, context):
    if check_in(update, context):
        id = context.bot.send_photo(
            chat_id=message.chat.id, photo=generate_qr(u.addr).getvalue(), caption=static_text.WALLET_ADDR.format(addr=u.addr), reply_markup=make_keyboard_for_cmd_top_up_wallet_usdt(), parse_mode="HTML")
        #context.bot.send_message( message.chat.id, static_text.WALLET_ADDR.format(addr=u.addr), reply_markup=make_keyboard_for_cmd_top_up_wallet_usdt(), parse_mode="HTML")
        u.message_id = id.message_id
        u.save()
    del_mes(update, context, True)

# Удаляем выставленный счет
def cmd_del_invoice_trc20(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    invoice = Invoice.objects.get(payer_id=u)
    invoice.delete()
    cmd_wallet(update, context)




###################################
###################################
def cmd_help(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    message = get_message_bot(update)

    id = context.bot.send_message(
        message.chat.id, static_text.HELP,
        reply_markup=make_keyboard_for_cmd_help(), parse_mode="HTML", disable_web_page_preview=True)
    u.message_id = id.message_id
    u.save()
    del_mes(update, context, True)


def cmd_admin(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    if u.is_admin:
        message = get_message_bot(update)
        id = context.bot.send_message(message.chat.id, static_text.ADMIN_MENU_TEXT.format(
            context.bot.get_chat_member(chat_id=-1001793015412, user_id=u.user_id)), reply_markup=make_keyboard_for_cmd_admin(), parse_mode="HTML")
        u.message_id = id.message_id
        u.save()
        del_mes(update, context, True)
    else:
        command_start(update, context)


def cmd_pass():
    pass


# словарь функций Меню по состоянию
State_Dict = {
    # Когда выбрано Меню, мы можем только нажимать кнопки. Любой текст удаляется
    static_state.S_MENU: del_mes,
    static_state.S_EMAIL: s_email,
}

# словарь функций Меню
Menu_Dict = {
    'Старт': command_start,
    'Меню': cmd_menu,
    'Кошелек': cmd_wallet,
    'Почта': chenge_email,
    'Пополнить_Кошелек_TRC20':cmd_top_up_wallet_usdt,
    'Удалить_invoice':cmd_del_invoice_trc20,
    'Администрирование': cmd_admin,
    'pass': cmd_pass,
    'Help': cmd_help,
}


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(
            updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
