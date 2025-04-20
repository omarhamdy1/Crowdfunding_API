from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import (
    MultiPartParser, FileUploadParser
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .tasks import send_email

from .models import Collect, Payment
from .serializers import (
    CollectSerializer, PaymentSerializer, RegisterSerializer
)


class RegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для регистрации пользователей.
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser, FileUploadParser]

    @swagger_auto_schema(
        manual_parameters=[
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
        responses={
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
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': {
                'username': user.username,
                'email': user.email
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FileUploadParser]

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)
        send_email.delay(
            subject='Новый сбор создан',
            message=f'Вы успешно создали сбор: {collect.title}',
            recipient_list=[self.request.user.email]
        )

    @swagger_auto_schema(
        manual_parameters=[
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
                description='Дата завершения сбора \
                             (формат: 2025-05-01T00:00:00)',
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
        responses={
            201: 'Сбор успешно создан',
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    http_method_names = ['get', 'post', 'delete']

    @swagger_auto_schema(
        manual_parameters=[
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
        responses={
            200: 'Пожертвование успешно добавлено'
        }
    )
    def create(self, request, *args, **kwargs):
        collect = Collect.objects.get(id=request.data.get('collect'))
        amount = int(request.data.get('amount'))
        payment = Payment.objects.create(
            user=request.user,
            collect=collect,
            amount=amount
        )
        collect.collected_amount += payment.amount
        collect.donors_count += 1
        collect.save()
        send_email.delay(
            subject='Новое пожертвование',
            message=f'Пользователь {request.user.username} '
                    f'пожертвовал {amount} на ваш сбор.',
            recipient_list=[collect.author.email]
        )
        return Response({'message': 'Пожертвование успешно добавлено'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        collect = instance.collect
        collect.collected_amount -= instance.amount
        collect.donors_count -= 1
        collect.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
