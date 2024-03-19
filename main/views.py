from rest_framework import viewsets
from .models import FarmerProfile, MarketplaceProduct, MarketplaceProductCategory, GovernmentProduct, GovernmentProductCategory
from .serializers import FarmerProfileSerializer, MarketplaceProductSerializer,MarketplaceProductCategorySerializer, GovernmentProductSerializer, GovernmentProductCategorySerializer
from django.http import JsonResponse
from gtts import gTTS
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MarketplaceProductOrder, GovernmentProductOrder
from .serializers import MarketplaceProductOrderSerializer, GovernmentProductOrderSerializer
import os
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
def test_func(request):
    context={

    }
    return render(request,'test.html',context)
class FarmerProfileViewSet(viewsets.ModelViewSet):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer


# ============================== Marketplace ===============================
class MarketplaceProductViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceProduct.objects.all()
    serializer_class = MarketplaceProductSerializer

class MarketplaceProductCategoryViewset(viewsets.ModelViewSet):
    queryset = MarketplaceProductCategory.objects.all()
    serializer_class = MarketplaceProductCategorySerializer

class MarketplaceProductOrderViewSet(viewsets.ModelViewSet):
    queryset = MarketplaceProductOrder.objects.all()
    serializer_class = MarketplaceProductOrderSerializer
    permission_classes = [IsAuthenticated]



# ============================== Product By Government =====================
class GovernmentProductViewSet(viewsets.ModelViewSet):
    queryset = GovernmentProduct.objects.all()
    serializer_class = GovernmentProductSerializer

class GovernmentProductCategoryViewset(viewsets.ModelViewSet):
    queryset = GovernmentProductCategory.objects.all()
    serializer_class = GovernmentProductCategorySerializer

class GovernmentProductOrderViewSet(viewsets.ModelViewSet):
    queryset = GovernmentProductOrder.objects.all()
    serializer_class = GovernmentProductOrderSerializer
    permission_classes = [IsAuthenticated]

# ============================== Online consultation =======================


# ============================== data training =============================


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