from drf_yasg import openapi

register_swagger_schema = {
    'manual_parameters': [
        openapi.Parameter(
            'username',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Имя пользователя',
            required=True
        ),
        openapi.Parameter(
            'email',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Email пользователя',
            required=True
        ),
        openapi.Parameter(
            'password',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Пароль пользователя',
            required=True
        ),
    ],
    'responses': {
        201: openapi.Response(
            description='Пользователь успешно создан',
            examples={
                "application/json": {
                    "user": {
                        "username": "john_doe",
                        "email": "user@example.com"
                    },
                    "refresh": "your-refresh-token",
                    "access": "your-access-token"
                }
            }
        ),
        400: 'Неверные данные'
    }
}

collect_create_swagger_schema = {
    'manual_parameters': [
        openapi.Parameter(
            'title',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Название сбора',
            required=True
        ),
        openapi.Parameter(
            'occasion',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Повод',
            enum=['birthday', 'wedding', 'charity', 'other'],
            required=True
        ),
        openapi.Parameter(
            'description',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Описание сбора',
            required=True
        ),
        openapi.Parameter(
            'target_amount',
            openapi.IN_FORM,
            type=openapi.TYPE_NUMBER,
            description='Целевая сумма',
            required=True
        ),
        openapi.Parameter(
            'end_date',
            openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATETIME,
            description='Дата завершения сбора (формат: 2025-05-01T00:00:00)',
            required=True
        ),
        openapi.Parameter(
            'cover_image',
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='Обложка сбора (изображение)',
            required=False
        ),
    ],
    'responses': {
        201: 'Сбор успешно создан',
    }
}

payment_create_swagger_schema = {
    'manual_parameters': [
        openapi.Parameter(
            'collect',
            openapi.IN_FORM,
            type=openapi.TYPE_NUMBER,
            description='id сбора',
            required=True
        ),
        openapi.Parameter(
            'amount',
            openapi.IN_FORM,
            type=openapi.TYPE_NUMBER,
            description='Сумма пожертвования',
            required=True
        ),
    ],
    'responses': {
        200: 'Пожертвование успешно добавлено'
    }
}
