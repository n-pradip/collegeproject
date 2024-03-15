from rest_framework import serializers
from .models import FarmerProfile, VendorProfile, MarketplaceProduct, Order, Message, MarketplaceProductCategory, GovernmentProduct, GovernmentProductCategory

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = '__all__'

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'

class MarketplaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProduct
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
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