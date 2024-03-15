from rest_framework import serializers
from .models import *
from menu.serializers import *

class DocumentSerializer(serializers.ModelSerializer):
    review_and_understood = serializers.SerializerMethodField()
    menu_title = serializers.ReadOnlyField(source="menu.title")
    sub_menu_title = serializers.ReadOnlyField(source="sub_menu.title")
    sub_menu_branch_title = serializers.ReadOnlyField(source="sub_menu_branch.title")
    # menu = MenuSerializer(read_only=True)
    # sub_menu = SubMenuSerializer(read_only=True)
    # sub_menu_branch = SubMenuBranchSerializer(read_only=True)
    class Meta:
        ref_name="document_serializer"
        model = Document
        fields = '__all__'
    
    def get_review_and_understood(self, obj):
        return self.context['request'].user in obj.user_review_and_understood.all()

class DocumentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentService
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

    def validate_name(self, value):
        if Subcategory.objects.filter(name=value).exists():
            raise serializers.ValidationError("Subcategory with this name already exists")
        return value

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        name = data.get('name')
        existing_categories = Category.objects.filter(name=name)
        if existing_categories.exists():
            raise serializers.ValidationError("Category already exists")
        
        subcategories_data = data.get('subcategories', [])
        for subcategory_data in subcategories_data:
            subcategory_name = subcategory_data.get('name')
            existing_subcategories = Subcategory.objects.filter(name=subcategory_name)
            if existing_subcategories.exists():
                raise serializers.ValidationError("Subcategory already exists")
        return data

    def create(self, validated_data):
        subcategories_data = validated_data.pop('subcategories', [])
        category = Category.objects.create(**validated_data)
        for subcategory_data in subcategories_data:
            Subcategory.objects.create(category=category, **subcategory_data)
        return category



class ADCDocumentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADCDocumentComment
        fields = '__all__'

class ADCDocumentSerializer(serializers.ModelSerializer):
    adc_comments = ADCDocumentCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ADCDocument
        fields = '__all__'

    def validate_docfile1(self, file):
        ADC_DOCUMENT_FILE_SIZE = 2  # in MB
        ADC_DOCUMENT_ALLOWED_EXTENSIONS = ['png', 'jpg', 'pdf']

        if not file:
            raise serializers.ValidationError("File not provided.")

        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in ADC_DOCUMENT_ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"Invalid file type. Allowed types are: {', '.join(ADC_DOCUMENT_ALLOWED_EXTENSIONS)}"
            )

        max_size_bytes = ADC_DOCUMENT_FILE_SIZE * 1024 * 1024  # Convert MB to bytes
        if file.size > max_size_bytes:
            raise serializers.ValidationError(
                f"File size exceeds the allowed limit of {ADC_DOCUMENT_FILE_SIZE} MB"
            )

        return file
