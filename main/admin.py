from django.contrib import admin
from .models import FarmerProfile, MarketplaceProduct, MarketplaceProductCategory, GovernmentProduct, GovernmentProductCategory

admin.site.register(FarmerProfile)
admin.site.register(MarketplaceProduct)
admin.site.register(MarketplaceProductCategory)
admin.site.register(GovernmentProduct)
admin.site.register(GovernmentProductCategory)
