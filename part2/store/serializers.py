from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

# difference between modelserializer and serializer is that modelserializer is used to serialize the model and serializer is used to serialize the data meaning it will suppurt the data that is not in the model

class CollectionSerializer(serializers.ModelSerializer): # this is subclass of serializers which is from rest_framework.
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count'] # this is used to serialize all the fields of the model
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    products_count = serializers.IntegerField(read_only=True) # this is used to add the extra field in the serializer
    # READ ONLY means you dont give permission for the users to post the data. it is only for the get request.
    

# class ProductSerializer(serializers.Serializer): # this is subclass of serializers which is from rest_framework.
#     # this is used to serialize the data which means to convert the data into json format which is dictionary and used to send the data
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')  # sometimes the field name in the model is different from the field name in the serializer so we can use source to map the field name 
#     price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax') # this is used to add the extra field in the serializer
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all() 
#     # ) # this is used to serialize the foreign key field. how it works: it will get the id of the collection and will serialize it.   
#     # collection = serializers.StringRelatedField()  # how it works: it will get the string representation of the collection and will serialize it.
#     # collection = CollectionSerializer() # how it works: it will get the collection object and will serialize it.    

    # # HYPER LINK TO ANOTHER OBJECT ---
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail' # create this view in the urls.py
    # ) # how it works: it will get the collection object and will serialize it.
#     def get_price_with_tax(self, product): # this method is used to calculate the price with tax
#         return product.unit_price * Decimal(1.1) # 10% tax. only decimal can be multiplied with decimal and float to float




class ProductSerializer(serializers.ModelSerializer): # this is basically the same as above but it is the subclass of ModelSerializer which is from rest_framework and it is less code
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax'] # in easy words this is used to serialize the fields of the model 
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax') # this is used to add the extra field in the serializer

    # # HYPER LINK TO ANOTHER OBJECT ---
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail' # create this view in the urls.py
    # ) # how it works: it will get the collection object and will serialize it.

    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    def get_price_with_tax(self, product): # this method is used to calculate the price with tax
        return product.unit_price * Decimal(1.1) # 10% tax. only decimal can be multiplied with decimal and float to float

    # def validate_title(self, data): # this is how we can overright the is_valid() method of the serializer
    #     if len(data['title']) < 10:
    #         raise serializers.ValidationError('Title must be at least 10 characters long')
    #     return value # this is another way of validating the data. this is used to validate the title field of the product
    #     return data

    # def create(self, validated_data): # this is how we can overright the save() method of the serializer
    #     product = Product(**validated_data)
    #     product.other_special_fields = 1
    #     product.save()
    #     return product # this is used to create the new product in the database

    # def update(self, instance, validated_data): # the save method will call the update method if the instance is already there and this is how we can overright the update method of the serializer
    #    instance.unit_price = validated_data.get('unit_price')
    #    instance.save()
    #    return instance
    