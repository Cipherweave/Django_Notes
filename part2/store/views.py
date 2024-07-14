from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # django has http request and responce, rest_framework has the same
# but more powerfull
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer 

# Create your views here.
@api_view(['GET', 'POST']) # this decorator is used to define the view by doing this we can use the rest_framework
def product_list(request):
    if request.method == 'GET':
        # return HttpResponse('ok') # this is the standard way of returning the response in django
        # return Response('ok') # this is the way of returning the response in rest_framework
        products = Product.objects.all() # get all the products from the database
        serializer = ProductSerializer(products, many=True, context={'request': request}) # many=True is used to serialize the multiple objects and in this case products is a queryset
        # context={'request': request} sends the hyperlinks in the response
        return Response(serializer.data) # serializer.data gives you the data in dict format
    elif request.method == 'POST': # this whole second part is used to create the new product when the requestion is basically adding to the database instead of getting the data
        serializer = ProductSerializer(data=request.data) # this is used to serialize the data that is coming from the request.
        #  Why does it use the same serializer as Get: because the data is coming in the same format as the data is going out so serilizer will serialize and deserialize the data at the same time
        # INSTEAD OF THIS:
        # if serializer.is_valid():
        #     serializer.validate() # the data is gonna be available in the serializer.validate()
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # WE CAN USE THIS:
        serializer.is_valid(raise_exception=True) # checks whether the user imput is currect or not. we can overwrite it in the serializer which we did as an example using def validate
        serializer.validated_data 
        return Response('ok')



@api_view()
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id) # get the product from the database
    #     serializer = ProductSerializer(product) # converting the data into json format
    #     return Response(serializer.data) # serializer.data gives you the data in dict format
    #     # the conversion of dict to json is done hiddenly by the rest_framework and by json renderer
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND) # if the product is not found then return 404 status code. 
    #     # this is the standard REST API status code

    # INSTED the same thing:
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_detail(request, pk):
    return Response('ok')