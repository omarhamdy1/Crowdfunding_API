from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import (
    MultiPartParser, FileUploadParser
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from .models import Collect, Payment
from .serializers import (
    CollectSerializer, PaymentSerializer, RegisterSerializer
)
from .services import (
    get_cached_data,
    generate_cache_key,
    clear_cache_keys,
    send_welcome_email,
    send_collect_creation_email,
    send_donation_email
)
from .swagger_schemas import (
    register_swagger_schema,
    collect_create_swagger_schema,
    payment_create_swagger_schema
)


class RegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для регистрации пользователей.
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FileUploadParser)

    @swagger_auto_schema(**register_swagger_schema)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        send_welcome_email(
            user=user, refresh_token=refresh, access_token=refresh.access_token
        )

        response_data = {
            'user': {
                'username': user.username,
                'email': user.email
            },
            'refresh': f'Bearer {refresh}',
            'access': f'Bearer {refresh.access_token}',
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CollectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления сборами.
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser)

    def list(self, request, *args, **kwargs):
        cache_key = generate_cache_key('collect_list', self.request.user.id)
        cached_data = get_cached_data(
            cache_key,
            query_fn=lambda: list(self.queryset.filter(
                author=self.request.user)
            ),
        )
        serializer = self.get_serializer(cached_data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = generate_cache_key(
            'collect_detail', self.request.user.id, instance.id
        )
        cached_data = get_cached_data(
            cache_key,
            query_fn=lambda: self.get_serializer(instance).data,
        )
        return Response(cached_data)

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)
        clear_cache_keys(
            generate_cache_key('collect_list', self.request.user.id),
        )
        send_collect_creation_email(
            user=self.request.user,
            collect_title=collect.title
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        clear_cache_keys(
            generate_cache_key(
                'collect_detail', self.request.user.id, instance.id
            ),
            generate_cache_key(
                'collect_list', self.request.user.id
            ),
        )

    def perform_destroy(self, instance):
        clear_cache_keys(
            generate_cache_key(
                'collect_detail', self.request.user.id, instance.id
            ),
            generate_cache_key(
                'collect_list', self.request.user.id
            ),
        )
        instance.delete()

    @swagger_auto_schema(**collect_create_swagger_schema)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    http_method_names = ('get', 'post', 'delete')

    @swagger_auto_schema(**payment_create_swagger_schema)
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

        clear_cache_keys(
            generate_cache_key('payment_list', self.request.user.id),
        )

        send_donation_email(
            donor_username=request.user.username,
            amount=amount,
            collect_title=collect.title,
            author_email=collect.author.email
        )
        return Response({'message': 'Пожертвование успешно добавлено'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        collect = instance.collect
        collect.collected_amount -= instance.amount
        collect.donors_count -= 1
        collect.save()

        clear_cache_keys(
            generate_cache_key(
                'payment_detail', self.request.user.id, instance.id
            ),
            generate_cache_key(
                'payment_list', self.request.user.id
            ),
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        cache_key = generate_cache_key('payment_list', self.request.user.id)
        cached_data = get_cached_data(
            cache_key,
            query_fn=lambda: list(
                self.queryset.filter(user=self.request.user)
            ),
        )
        serializer = self.get_serializer(cached_data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = generate_cache_key(
            'payment_detail', self.request.user.id, instance.id
        )
        cached_data = get_cached_data(
            cache_key,
            query_fn=lambda: self.get_serializer(instance).data,
        )
        return Response(cached_data)

    def perform_update(self, serializer):
        instance = serializer.save()
        clear_cache_keys(
            generate_cache_key(
                'payment_detail', self.request.user.id, instance.id
            ),
            generate_cache_key(
                'payment_list', self.request.user.id
            ),
        )

    def perform_destroy(self, instance):
        clear_cache_keys(
            generate_cache_key(
                'payment_detail', self.request.user.id, instance.id
            ),
            generate_cache_key(
                'payment_list', self.request.user.id
            ),
        )
        instance.delete()
