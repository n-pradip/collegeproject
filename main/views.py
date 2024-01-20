from rest_framework import viewsets
from .models import FarmerProfile, VendorProfile, Product, Order, Message, ProductCategory
from .serializers import FarmerProfileSerializer, VendorProfileSerializer, ProductSerializer, OrderSerializer, MessageSerializer,ProductCategorySerializer

class FarmerProfileViewSet(viewsets.ModelViewSet):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer

class VendorProfileViewSet(viewsets.ModelViewSet):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCategoryViewset(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


from django.http import JsonResponse
from gtts import gTTS
import os
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_text_to_speech(request, product_id):
    product = Product.objects.get(id=product_id)

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