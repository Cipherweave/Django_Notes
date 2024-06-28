from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer

# Create your views here.

def say_hello(request):

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

    queryset = Product.objects.filter(description__isnull=True) # this is used to filter by null values. means all products the description is null

    queryset2 = Customer.objects.filter(email__contains='.com')

    # return HttpResponse('Hello, Django!')
    return render(request, 'hello.html', { 'name': 'Django', 'products': list(queryset), 'customers': list(queryset2)})