import logging
import requests

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)

API_URL = settings.SMTP_BZ_API_URL
API_KEY = settings.SMTP_BZ_API_KEY


@shared_task
def send_email(subject, message, recipient_list):
    """
    Отправляет email через внешний SMTP API.
    """
    payload = {
        'name': 'Crowdfunding Service',
        'from': settings.DEFAULT_FROM_EMAIL,
        'subject': subject,
        'to': recipient_list[0],
        'text': message,
    }

    headers = {
        'Authorization': f'{API_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            logger.info(
                f'Письмо успешно отправлено '
                f'получателю(ям): {", ".join(recipient_list)}'
            )
        else:
            logger.error(
                f'Ошибка при отправке письма '
                f'получателю(ям) {", ".join(recipient_list)}: '
                f'Статус {response.status_code}, Ответ: {response.text}'
            )
    except Exception as e:
        logger.error(
            f'Ошибка при отправке письма '
            f'получателю(ям) {", ".join(recipient_list)}: {str(e)}'
        )
