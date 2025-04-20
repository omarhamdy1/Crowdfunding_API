from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterViewSet, CollectViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('collects', CollectViewSet, basename='collects')
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]
