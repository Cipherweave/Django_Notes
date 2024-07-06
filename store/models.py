from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Parent classes have to always be defined before the child classes
# This is because the child classes have a foreign key to the parent classes
# else you will get an error
# however you can use the string representation of the parent class in the child class if this rule cannot be followed


# you only need to put the foreign key (many to one) in the child class if the child class is the many side of the relationship
# because django automatically creates a reverse relationship for you


class Promotion(models.Model):
    desctiption = models.CharField(max_length=255)
    discount = models.FloatField()  # float
    # products which is all the products that have this promotion

    def __str__(self) -> str:
        return self.desctiption
    
    class Meta:
        ordering = ['discount']


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+")  
    # foreign key to the product table. the related_name="+" is used to prevent django from creating a reverse relationship

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


# Create your models here.
class Product(models.Model):  # these fields are all in https://docs.djangoproject.com/en/5.0/ref/models/fields/ 
    # sku = models.CharField(max_length=255, unique=True)  # the reason we dont have the id is because django automatically creates an id field for us but we can override it
    title = models.CharField(max_length=255)  # varchar(255)
    slug = models.SlugField()  # slug is a field that is used to create a url friendly version of the title it is used for seo
    # and goes on the url to make it more readable for search engines. slogfield works by converting the title to lowercase
    description = models.TextField(null=True, blank=True)  # text. blank=True means that the field can be empty in the admin site
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(1)]) # decimal(6,2)  is like 9999.99, validators is used to add a constraint to the field in this case the minimum value is 1
    inventory = models.IntegerField(validators=[MinValueValidator(1)])  # int
    last_update = models.DateTimeField(auto_now=True)  # datetime
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)  # on_delete in this case is used to protect the collection from being deleted
    promotions = models.ManyToManyField(Promotion, related_name='product', blank=True)  # many to many relationship with the promotion table
    # because a product can have multiple promotions and a promotion can be applied to multiple products
    # related_name is the name given to the reverse relationship that django creates for us
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [  # used for the membership 
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    test = models.CharField(max_length=255, null=True)  # this is used to test the migrations
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # varchar(255) with a unique constraint
    phone = models.CharField(max_length=255)  # varchar(20)
    birth_date = models.DateField(null=True)  # date
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE) # used the choices list
    # address = ... # we dont need to add address here because django already created one for use (the reverse relationship)
    # class Meta: # class meta is as an setting for the model (table)
    #     db_table = 'store_customers'  # this is used to change the name of the table in the database
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name'])  # this is used to create an index on the last_name and first_name fields
    #     ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']

class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAILD = 'F'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (FAILD, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # foreign key to the customer table

    def __str__(self) -> str:
        return f"Order {self.placed_at}"
    
    class Meta:
        ordering = ['-placed_at']


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Cart {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']

class Address(models.Model): # Child of the customer table
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=20, null=True)   
    # -- one to one relationship
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)  # one to one relationship
    # with the parent customer table. if you dont want to delete the customer when the customer obj is deleted you can use on_delete=models.SET_NULL
    # if we want to say address (child) should be deleted before the customer (parent) is deleted we can use
    #  on_delete=models.PROTECT   it depends on the use case


    # -- one to many relationship
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # one to many relationship
    # means that a customer can have multiple addresses but an address can only have one customer

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip}"
    
    class Meta:
        ordering = ['state', 'city', 'street']


class OrderItem(models.Model):  # child of the order table
    order = models.ForeignKey(Order, on_delete=models.PROTECT)  # foreign key to the order table
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # foreign key to the product table
    quantity = models.PositiveSmallIntegerField() # positive small integer
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)  # this is dues to the fact that the price of the 
    # product can change after the order has been placed

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"
    
    class Meta:
        ordering = ['order']


class CartItem(models.Model):  # child of the cart table
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # foreign key to the cart table
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # foreign key to the product table
    quantity = models.PositiveSmallIntegerField()  # positive small integer

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity}"
    
    class Meta:
        ordering = ['cart']





