from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.db.models.fields import DecimalField
from django.db import transaction
from django.db import connection # for cursor
from store.models import Product, Customer, OrderItem, Order, Collection, CartItem, Cart
from tags.models import TaggedItem

# Create your views here.


@transaction.atomic() # the transaction func is used as a decorator. decorator means that if there is an error in the code then it will rollback the transaction
def say_hello(request):

    """ THIS IS THE NOTE SECTION"""

    # query_set = Product.objects.all()    # this is a query set and works like a list of products in the database
    # # however it is just a bunch of queries that have not been executed yet
    # print(query_set)  # this prints out the query that is being executed (SELECT * FROM store_product) but 
    # # there is a limit to how many products are selected.
    # # for product in query_set: # this is a for loop that goes through the query set
    # #     print(product)


    # try:
    #     product = Product.objects.get(pk=0) # filter with primary key
    # except ObjectDoesNotExist:
    #     pass
    
    # product = Product.objects.filter(pk=0).first() # this is the same as the above code but we dont get error

    # exists = Product.objects.filter(pk=0).exists()  # this checks if the product exists with boolean value

    # queryset = Product.objects.filter(unit_price__gt=20) # means greater than 20 because of the __gt
    # queryset = Product.objects.filter(unit_price__lt=20) # means less than 20 because of the __lt
    # queryset = Product.objects.filter(unit_price__gte=20) # means greater than or equal to 20 because of the __gte
    # queryset = Product.objects.filter(unit_price__lte=20) # means less than or equal to 20 because of the __lte
    # queryset = Product.objects.filter(unit_price__range=(10, 20)) # means between 10 and 20 because of the __range
    # queryset = Product.objects.filter(unit_price__in=[10, 20, 30]) # means in the list of 10, 20, 30 because of the __in  

    # queryset = Product.objects.filter(title__icontains='coffee') # i means case insensitive and contains means it contains the word coffee
    # # insensitive means it either upper or lower case.

    # queryset = Product.objects.filter(last_update__year=2021) # this is used to filter by year

    # queryset = Product.objects.filter(description__isnull=True) # this is used to filter by null values. means all products the description is null

    queryset2 = Customer.objects.filter(email__contains='.com')

    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20) # this is basicly double filtering. like using AND operator
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20) # this is the same as the above code

    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20)
    #     ) # this is basicly using OR operator   also ~Q() is used for NOT operator
    
    # queryset = Product.objects.filter(inventory__lt=F('unit_price')) # this is how we compare two columns in the same table

    # queryset = Product.objects.order_by('unite_price' ,'-title') # To order the products by mutiple columns we use a comma
    # # to change the order to descending order we use the '-' sign like (-'title')
    # # .reverse() at the end is used to reverse the order of the products

    # queryset = Product.objects.filter(collection__id=1).order_by('unite_price') # we can also filter while usig order_by

    # product = Product.objects.order_by('unite_price')[0] # as soon as we pick the first item,
    # # django executes the query and returns the first item therefor we name it product

    # product = Product.objects.earliest('unite_price') # same the above 
    # product = Product.objects.latest('unite_price') # opposite of the above

    # queryset = Product.objects.all()[:5] # the limit and get the first 5 products index: 0-4
    # queryset = Product.objects.all()[5:10] # the limit and get the next 5 products index: 5-9

    # queryset = Product.objects.values('title', 'unit_price', 'collection__title') # this is used to get the columns we want like select title, unit_price from product
    # # once we use values, then we dont have product instances anymore but dictionaries.

    # # this doesnt work----
    # queryset = OrderItem.objects.values('product_id', 'Product__title').distinct.order_by('Product__title') 

    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product_id').distinct()).order_by('title') # this is used to get the products that have been ordered

    # queryset = Product.objects.only('title') # this is similar to values but it returns product instances
    # # there is a catch with this and that it will create a query for each product instance if we give it a column name that is not specified in the only method

    # queryset = MyModel.objects.only('field1', 'field2') # this returns only the field1 and field2 columns
    # queryset = MyModel.objects.defer('large_field') this returns everything except the large_field

    # queryset = Product.objects.select_related('collection').all() # this is how we select the related tables (objects)
    # # we could use mutiple select_related like select_related('collection', 'promotions')
    # # selected_related is for One to Many relationships like collection for example each product can have only one collection
    # # prefetch_related is for Many to Many relationships like promotions for example each item can have multiple promotions
    # queryset = Product.objects.prefetch_related('promotions').all() # this is how we select the related tables (objects)


    # queryset = Order.objects.all().select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # # the orderitem_set is the name of the reverse relationship that django created for us, __product is the name of the table we want to get

    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price')) # cound the number of products. this returns a dictionary
    # # count is the name of the key. we could use aggregates at the end of the querysets too.

    # result = Order.objects.aggregates(count=Count('id')) # this is how we count the number of orders
    # result = OrderItem.objects.filter('product__id' == 1).aggregates(sum=Sum('quantity')) # this is how we sum the quantity of the products

    # queryset = Customer.objects.annotate(is_new=Value(True))  # we beasically use annotate to give a new column to the the table
    # # in this case is_new in this queryset. it doesn not affect the actual table in the database

    # queryset = Customer.objects.annotate(new_id=F('id')) # So this creates a new column called new_id and copies the id column to it    
    # # Django only gets expressions as arguments so for example it doesnt acdept True by itself.
    # # So we use Value(True) instead or for fields we use F('id') instead of just 'id'


    # queryset = Customer.objects.annotate(
    #     full_name=Func(
    #         F('first_name'), Value(' '), F('last_name'), function='CONCAT'
    #     )
    # ) # this is how we concatenate two columns in the table using the functions in this case CONCAT

    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # ) # this is another way to concatenate two columns in the table using the Concat function
    # # more functions on: https://docs.djangoproject.com/en/5.0/ref/models/database-functions/

    # queryset = Customer.objects.annotate(
    #     order_count=Count('order')
    # ) # this is how we count the number of orders each customer has


    # queryset = Product.objects.annotate(
    #     discounted_price=F('unit_price') * 0.8
    # ) # this gives error because we are trying to multiply a field by a number
    # # expressionwrapper makes everything into one object
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discounted_price) # this is how we add a new column to the table

    # queryset2 = Customer.objects.annotate(last_order_id=Max('order__id')) # this is how we get the last order id for each customer

    # queryset = Collection.objects.annotate(product_count=Count('product')) # this is how we count the number of products in each collection

    # queryset = Customer.objects.annotate(order_count=Count('order__id')).filter(order_count__gt=5) # this is how we filter the customers that have more than 5 orders

    # queryset = Customer.objects.annotate(total_spent=Sum(
    #     F('order__orderitem__unit_price') * F('order__orderitem__quantity')
    # ))

    queryset = Product.objects.annotate(total_sell=Sum(
        F('orderitem__unit_price') * F('orderitem__quantity')
    )).order_by('-total_sell')[:5] # this is how we get the top 5 products that have been sold the most

    # Content_type = ContentType.objects.get_for_model(Product) # we need content type to get the id of the content in this case product
    # queryset = TaggedItem.objects \
    #     .select_related('tag') \
    #     .filter(
    #         content_type=Content_type,
    #         object_id=1
    #     ) # this is how we get the tags for a product

    # # AN EASIER WAY ---

    # # we create a custom manager in the tags/models.py file then we can use it like this
    # TaggedItem.objects.get_tags_for(Product, 1) 


    # HOW CACHE WORKS ---- 
    # when we create a query set, it read the data from the database which is slow. However once
    # it read the data, it stores it in the cache in the memory which is fast. So if we do the same query again.
    # however if we have query that contains a large amount of data outside the scope the prev one then it will
    # have to create a new query and store it in the cache. so make the big query first and then the small query


    #  HOW TO SAVE DATA ----
    # Collection = Collection()
    # Collection.title = 'Video Games'
    # Collection.featured_product = Product.objects.get(pk=1)
    # Collection.save() # this is how we save the collection

    # # Another way to save the collection but the problem is that if we rename fields in the model then we have 
    # # to change the code but the above code is more dynamic
    # Collection.objects.create(title='Video Games', featured_product=Product.objects.get(pk=1)) 

    # HOW TO UPDATE DATA ----
    # Collection = Collection.objects.get(pk=1)
    # Collection.featured_product = None
    # Collection.save() # this is how we save the collection

    # # Another way to update the collection:
    # Collection.objects.update(featured_product=None) # for all the collections
    # Collection.objects.filter(pk=11).update(featured_product=None)


    # HOW TO DELETE DATA ----
    # collection = Collection.objects.get(pk=12)
    # collection.delete()
    # Or...
    # Collection.objects.filter(id=11).delete() 

    # # create a shoping cart
    # cart = Cart()
    # cart.save()   
    # cart_item = CartItem()
    # cart_item.cart = cart
    # cart_item.product = Product.objects.get(pk=1)
    # cart_item.quantity = 2
    # cart_item.save()

    # # update the quantity of the cart item
    # cart_item = CartItem.objects.get(pk=1)
    # cart_item.quantity = 3
    # cart_item.save()


    # # delete the cart item and cart all together
    # cart = Cart.objects.filter(pk=2)
    # cart.delete()   

    # # TRANSACTION ----
    # with transaction.atomic(): # this is the second way to use the transaction function. first way was as a decorator
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1  # if we for example give -1 then it will give an error because it is a positive small integer and the code inside the transaction will be rolled back
    #     item.unit_price = 10
    #     item.save()

    # # EXECUTING RAW SQL ----
    # Product.objects.raw('SELECT * FROM store_product WHERE unit_price > 20') # this is how we execute raw sql
    # # We use this if we want to use a sql query that is not supported by django or if we want to use a sql query that is faster than the django query

    # # USING CURSOR ---- 
    # # what is the difference between cursor and raw sql is that cursor is used to execute multiple queries at once like: 
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM store_product WHERE unit_price > 20')
    #     # cursor.callproc('store_report', [2021]) # this is how we call a stored procedure in the database
        



    # return HttpResponse('Hello, Django!')
    return render(request, 'hello.html', { 'name': 'Django', 'products': list(queryset), 'customers': list(queryset2)})