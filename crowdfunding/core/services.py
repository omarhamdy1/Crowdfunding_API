from .tasks import send_email


def send_generic_email(subject, message, recipient_list):
    """
    Универсальная функция для отправки писем через Celery.
    """
    send_email.delay(
        subject=subject,
        message=message,
        recipient_list=recipient_list
    )


def send_welcome_email(user, refresh_token, access_token):
    """
    Отправляет приветственное письмо новому пользователю.
    """
    subject = 'Добро пожаловать!'
    message = (
        f'Вы успешно зарегистрировали аккаунт: {user.username} \n'
        f'Ваш refresh-токен: Bearer {refresh_token} \n'
        f'Ваш access-токен: Bearer {access_token}'
    )
    recipient_list = (user.email,)
    send_generic_email(subject, message, recipient_list)


def send_collect_creation_email(user, collect_title):
    """
    Отправляет письмо о создании нового сбора.
    """
    subject = 'Новый сбор создан!'
    message = f'Вы успешно создали сбор: {collect_title}'
    recipient_list = (user.email,)
    send_generic_email(subject, message, recipient_list)


def send_donation_email(donor_username, amount, collect_title, author_email):
    """
    Отправляет письмо автору сбора о новом пожертвовании.
    """
    subject = 'Новое пожертвование!'
    message = (
        f'Пользователь {donor_username} '
        f'пожертвовал {amount} на ваш сбор "{collect_title}".'
    )
    recipient_list = (author_email,)
    send_generic_email(subject, message, recipient_list)
