from django.core.cache import cache

from .tasks import send_email


def get_cached_data(cache_key, query_fn, timeout=60 * 15):
    """
    Получает данные из кэша или базы данных.
    Если данных нет в кэше, выполняет запрос к базе данных
    и сохраняет результат в кэш.
    """
    cached_data = cache.get(cache_key)
    if cached_data is None:
        cached_data = query_fn()
        cache.set(cache_key, cached_data, timeout=timeout)
    return cached_data


def generate_cache_key(key_prefix, user_id=None, obj_id=None):
    """
    Генерирует ключ для кэша на основе префикса,
    ID пользователя и ID объекта.
    """
    if user_id and obj_id:
        return f"{key_prefix}_{obj_id}_{user_id}"
    elif user_id:
        return f"{key_prefix}_{user_id}"
    return key_prefix


def clear_cache_keys(*cache_keys):
    """
    Очищает указанные ключи кэша.
    """
    for key in cache_keys:
        cache.delete(key)


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
