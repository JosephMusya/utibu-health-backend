from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, DosageViewSet, OrderApiViewSet, RegisterView,UserViewSet
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

router = DefaultRouter()

router.register(f'orders', OrderApiViewSet, basename='orders')
router.register(f'dosage', DosageViewSet, basename='dosage')
router.register(f'my-cart', CartViewSet, basename="cart")
router.register(f'users', UserViewSet, basename="users")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name="register")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls