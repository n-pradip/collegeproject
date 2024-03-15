from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerProfileViewSet, VendorProfileViewSet, MarketplaceProductViewSet, OrderViewSet, MessageViewSet, MarketplaceProductCategoryViewset, GovernmentProductViewSet, GovernmentProductCategoryViewset
from blog.views import NoticeViewset
router = DefaultRouter()
# router.register(r'farmer-profiles', FarmerProfileViewSet)
# router.register(r'vendor-profiles', VendorProfileViewSet)
router.register(r'marketplaceproduct-category', MarketplaceProductCategoryViewset)
router.register(r'marketplaceproducts', MarketplaceProductViewSet)
router.register(r'governmentproduct-category', GovernmentProductCategoryViewset)
router.register(r'governmentproducts', GovernmentProductViewSet)

router.register(r'notice', NoticeViewset, basename='notice')
# router.register(r'orders', OrderViewSet)
# router.register(r'messages', MessageViewSet)

# router.register(r'speech', SpeechViewSet, basename='speech')

urlpatterns = [
    path('api/', include(router.urls)),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
]
