import logging

import requests
from django.conf import settings

logger = logging.getLogger('backend')


def send_error_to_telegram_group(message):
    if settings.TELEGRAM_CHAT_ID and settings.TELEGRAM_CHAT_TOKEN:
        try:
            url = (f"https://api.telegram.org/bot{settings.TELEGRAM_CHAT_TOKEN}/sendMessage?"
                   f"chat_id={settings.TELEGRAM_CHAT_ID}&text={message[:1000]}")
            print(requests.get(url).json())
        except Exception as ex:
            logger.exception(f'[+] send_error_to_telegram_group -> error', extra=dict(ex=ex))
