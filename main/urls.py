from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerProfileViewSet, VendorProfileViewSet, ProductViewSet, OrderViewSet, MessageViewSet, ProductCategoryViewset

router = DefaultRouter()
router.register(r'farmer-profiles', FarmerProfileViewSet)
router.register(r'vendor-profiles', VendorProfileViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'product-category', ProductCategoryViewset)
# router.register(r'speech', SpeechViewSet, basename='speech')

urlpatterns = [
    path('api/', include(router.urls)),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
]
