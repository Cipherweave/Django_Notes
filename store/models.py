from django.db import models

# Create your models here.
class Product(models.Model):  # these fields are all in https://docs.djangoproject.com/en/5.0/ref/models/fields/ 
    # sku = models.CharField(max_length=255, unique=True)  # the reason we dont have the id is because django automatically creates an id field for us but we can override it
    title = models.CharField(max_length=255)  # varchar(255)
    description = models.TextField()  # text
    price = models.DecimalFields(max_digits=6, decimal_places=2)  # decimal(6,2)  is like 9999.99
    inventory = models.IntegerField()  # int
    last_update = models.DateTimeField(auto_now=True)  # datetime
    
    
    
    
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # varchar(255) with a unique constraint
    phone = models.CharField(max_length=255)  # varchar(20)
    birthdate = models.DateField(null=True)  # date