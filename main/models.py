from django.db import models
from accounts.models import User
 

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_location = models.CharField(max_length=255)
    bio = models.TextField()
    contact_information = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    business_details = models.TextField()
    contact_information = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class MarketplaceProductCategory(models.Model):
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name
    
class GovernmentProductCategory(models.Model):
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name

class MarketplaceProduct(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    category = models.ForeignKey(MarketplaceProductCategory, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    discount = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class GovernmentProduct(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    category = models.ForeignKey(GovernmentProductCategory, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(MarketplaceProduct)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"
