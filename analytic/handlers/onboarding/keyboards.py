from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def make_keyboard_for_start(url = '') -> InlineKeyboardMarkup:
    if url == '':
        buttons = [
            [
                InlineKeyboardButton(text='✅ Продолжить', callback_data='Меню'),
            ],
        ]
    if url != '':
        buttons = [
            [
                InlineKeyboardButton(text='✅ Продолжить', url=url),
            ],
        ]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_check_username() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text='✅ Продолжить', callback_data='Меню')
    ]]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_check_in() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text='💻 Перейти в канал', url='https://t.me/+KoCswat85gBmNjQ6')
    ],[
        InlineKeyboardButton(text='✅ Продолжить', callback_data='Меню')
    ]]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_cmd_menu(adm) -> InlineKeyboardMarkup:
        buttons = []
        
        btn_help = InlineKeyboardButton(text='🆘 Помощь', url='https://t.me/serg_p2p')
       
        buttons.append([btn_help])
        
        if adm:
            btn_admin = InlineKeyboardButton(
                text='📝 Администрирование', callback_data="Администрирование")
            buttons.append([btn_admin])
        return InlineKeyboardMarkup(buttons)

def make_keyboard_for_cmd_help() -> InlineKeyboardMarkup:
    buttons = []
    btn_back = InlineKeyboardButton(text='⏪ Назад', callback_data='Меню')
    btn_main = InlineKeyboardButton(text='⏮ В начало', callback_data='Старт')
    buttons.append([btn_main, btn_back])
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_cmd_admin() -> InlineKeyboardMarkup:
    buttons = []
    btn_add_camp = InlineKeyboardButton(text='❇️ Добавить компанию', callback_data='Добавить_компанию')
    btn_rem_camp = InlineKeyboardButton(text='❌ Удалить компанию и всех пользователей', callback_data='Удалить_компанию')
    btn_back = InlineKeyboardButton(text='⏪ Назад', callback_data='Меню')
    btn_main = InlineKeyboardButton(
        text='⏮ В начало', callback_data='Старт')
    buttons.append([btn_add_camp])
    buttons.append([btn_rem_camp])
    buttons.append([btn_main, btn_back])
    return InlineKeyboardMarkup(buttons)