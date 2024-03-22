from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from gtts import gTTS
from rest_framework.permissions import IsAuthenticated
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import render

def test_func(request):
    context={

    }
    return render(request,'test.html',context)
class FarmerProfileViewSet(viewsets.ModelViewSet):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(MarketplaceProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_location = models.CharField(max_length=128,null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"


# ============================== Marketplace ===============================
class MarketplaceProductViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceProduct.objects.all()
    serializer_class = MarketplaceProductSerializer

class MarketplaceProductCategoryViewset(viewsets.ModelViewSet):
    queryset = MarketplaceProductCategory.objects.all()
    serializer_class = MarketplaceProductCategorySerializer

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class GovernmentProductViewSet(viewsets.ModelViewSet):
    queryset = GovernmentProduct.objects.all()
    serializer_class = GovernmentProductSerializer

class GovernmentProductCategoryViewset(viewsets.ModelViewSet):
    queryset = GovernmentProductCategory.objects.all()
    serializer_class = GovernmentProductCategorySerializer



@csrf_exempt
def generate_text_to_speech(request, product_id):
    product = MarketplaceProduct.objects.get(id=product_id)

    product_info_ne = product.name+" को मूल्य" + str(product.price)+ " " + "अगाडि जानको लागि हरियो बटनमा क्लिक गर्नुहोस्"

    from django.conf import settings
    tts = gTTS(text=product_info_ne, lang='ne')
    audio_path = os.path.join(settings.MEDIA_ROOT, f'product_audio/{product_id}_ne.mp3')

    directory = os.path.dirname(audio_path)
    os.makedirs(directory, exist_ok=True)
    tts.save(audio_path)
    tts = gTTS(text=product_info_ne, lang='ne')
    audio_path = f'media/product_audio/{product_id}_ne.mp3'
    tts.save(audio_path)
    return JsonResponse({'audio_url': audio_path})


#=============================== recommendation algorithm ================================
# views.py
from django.db.models import Avg
from .models import ProductRating

def get_recommendations(user):
    # Get products rated by the user
    rated_products = ProductRating.objects.filter(user=user)

    # Calculate average rating for each product
    product_ratings = {}
    for rating in rated_products:
        if rating.product not in product_ratings:
            product_ratings[rating.product] = []
        product_ratings[rating.product].append(rating.rating)

    # Calculate average rating for each product
    for product, ratings in product_ratings.items():
        product.average_rating = sum(ratings) / len(ratings)

    # Sort products by average rating
    sorted_products = sorted(product_ratings.keys(), key=lambda x: x.average_rating, reverse=True)

    # Return top recommended products
    return sorted_products[:5]

# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MarketplaceProduct
from .serializers import MarketplaceProductSerializer

@api_view(['GET'])
def recommend_products(request):
    user = request.user  # Assuming user is authenticated
    recommended_products = get_recommendations(user)
    serializer = MarketplaceProductSerializer(recommended_products, many=True)
    return Response(serializer.data)