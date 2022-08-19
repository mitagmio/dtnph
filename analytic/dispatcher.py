"""
    Telegram event handlers
"""
import sys
import logging
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.celery import app  # event processing in async mode
from dtb.settings import TELEGRAM_TOKEN_2, DEBUG, TELEGRAM_WEBHOOK_SECRET_2, TELEGRAM_WEBHOOK_URL

from analytic.handlers.utils import files, error
from analytic.handlers.onboarding import handlers as onboarding_handlers
from analytic import tasks as onboarding_handler_task


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    
    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # onboarding other handlers
    dp.add_handler(MessageHandler(Filters.text, onboarding_handlers.message_handler_func))
    dp.add_handler(MessageHandler(Filters.photo, onboarding_handlers.message_handler_func))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.callback_inline))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                   onboarding_handlers.status_handler_func))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN_2, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN_2).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN_2)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN_2.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',
            'stats': 'Statistics of bot 📊',
            'admin': 'Show admin info ℹ️',
            'ask_location': 'Send location 📍',
            'broadcast': 'Broadcast message 📨',
            'export_users': 'Export users.csv 👥',
        },
        'es': {
            'start': 'Iniciar el bot de django 🚀',
            'stats': 'Estadísticas de bot 📊',
            'admin': 'Mostrar información de administrador ℹ️',
            'ask_location': 'Enviar ubicación 📍',
            'broadcast': 'Mensaje de difusión 📨',
            'export_users': 'Exportar users.csv 👥',
        },
        'fr': {
            'start': 'Démarrer le bot Django 🚀',
            'stats': 'Statistiques du bot 📊',
            'admin': "Afficher les informations d'administrateur ℹ️",
            'ask_location': 'Envoyer emplacement 📍',
            'broadcast': 'Message de diffusion 📨',
            "export_users": 'Exporter users.csv 👥',
        },
        'ru': {
            'start': 'Запустить django бота 🚀',
            'stats': 'Статистика бота 📊',
            'admin': 'Показать информацию для админов ℹ️',
            'broadcast': 'Отправить сообщение 📨',
            'ask_location': 'Отправить локацию 📍',
            'export_users': 'Экспорт users.csv 👥',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
#set_up_commands(bot)

if TELEGRAM_WEBHOOK_URL == None:
    bot.delete_webhook()
else:
    url = "%s%s" % (TELEGRAM_WEBHOOK_URL,TELEGRAM_WEBHOOK_SECRET_2)

    if bot.get_webhook_info().url != url:
        bot.delete_my_commands(language_code='ru')
        bot.delete_my_commands(language_code='en')
        bot.delete_my_commands(language_code='es')
        bot.delete_my_commands(language_code='fr')
        bot.delete_my_commands()

        bot.delete_webhook()
        bot.set_webhook(url)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
