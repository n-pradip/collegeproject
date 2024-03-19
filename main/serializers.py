from rest_framework import serializers
from .models import FarmerProfile, MarketplaceProduct, MarketplaceProductCategory, GovernmentProduct, GovernmentProductCategory, MarketplaceProductOrder, GovernmentProductOrder

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = '__all__'

class MarketplaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProduct
        fields = '__all__'

class MarketplaceProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProductCategory
        fields = '__all__'

class GovernmentProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentProductCategory
        fields = '__all__'

class GovernmentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentProduct
        fields = '__all__'


class MarketplaceProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProductOrder
        fields =  '__all__'

class GovernmentProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentProductOrder
        fields = '__all__'
