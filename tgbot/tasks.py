"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
from datetime import datetime
from typing import Union, List, Optional, Dict

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.models import Settings, User

from dtb.celery import app
from celery.utils.log import get_task_logger
from tgbot.handlers.broadcast_message.utils import _send_message, _del_message, \
    _from_celery_entities_to_entities, _from_celery_markup_to_markup

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_message(
    user_ids: List[Union[str, int]],
    text: str,
    entities: Optional[List[Dict]] = None,
    reply_markup: Optional[List[List[Dict]]] = None,
    sleep_between: float = 0.4,
    parse_mode=telegram.ParseMode.HTML,
) -> None:
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{text}' to {len(user_ids)} users")

    entities_ = _from_celery_entities_to_entities(entities)
    reply_markup_ = _from_celery_markup_to_markup(reply_markup)
    for user_id in user_ids:
        try:
            _send_message(
                user_id=user_id,
                text=text,
                entities=entities_,
                parse_mode=parse_mode,
                reply_markup=reply_markup_,
            )
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")

@app.task(ignore_result=True)
def payment() -> None:
    """ Подтверждаем оплату по выставленным счетам  """
    logger.info("Starting payment invoices")
    settings = Settings.objects.get(id=1)
    logger.info(
        f"min_timestamp {int(settings.last_time_payment)}")
    try:
        Transactions = Invoice.get_payment(
            int(settings.last_time_payment))['data']
        logger.info(
            f"Transactions {Transactions}")
    except Exception as e:
        Transactions = dict()
        logger.info(
            f"Transactions {len(Transactions)}, reason: {e}")
    if len(Transactions) > 0:
        timeblock = 0
        for t in Transactions:
            if int(t['block_timestamp']) > timeblock:
                timeblock = int(t['block_timestamp'])
            pay_value = float(t['value']) / \
                10**float(t['token_info']['decimals'])

            try:
                inv = Invoice.objects.get(summ_invoice=pay_value)
            except Invoice.DoesNotExist:
                inv = None
            if inv != None:
                u = inv.payer_id
                u.balance += pay_value
                text = '💵 Ваш платеж на сумму <code>{}</code> USDT зачислен.\n\nТекущий баланс составляет <code>{}</code> USDT'.format(
                    pay_value, u.balance)
                _send_message(
                    user_id=u.user_id,
                    text=text,
                    entities=None,
                    parse_mode=telegram.ParseMode.HTML,
                    reply_markup=None,
                )
                time.sleep(0.1)
                u.save()
                inv.delete()
        settings.last_time_payment = timeblock + 1000
        settings.save()
    logger.info("Payment invoices was completed!")
