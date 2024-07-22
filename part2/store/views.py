from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view  # django has http request and responce, rest_framework has the same but more powerfull
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView # this is the class based view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet    
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer

# # FUNCTION BASED VIEW ---------------- LEVEL 1 ---------------- 
# # Create your views here.
# @api_view(['GET', 'POST']) # this decorator is used to define the view by doing this we can use the rest_framework
# def product_list(request):
#     if request.method == 'GET':
#         # return HttpResponse('ok') # this is the standard way of returning the response in django
#         # return Response('ok') # this is the way of returning the response in rest_framework
#         products = Product.objects.all() # get all the products from the database
#         serializer = ProductSerializer(products, many=True, context={'request': request}) # many=True is used to serialize the multiple objects and in this case products is a queryset
#         # context={'request': request} sends the hyperlinks in the response
#         return Response(serializer.data) # serializer.data gives you the data in dict format
#     elif request.method == 'POST': # this whole second part is used to create the new product when the requestion is basically adding to the database instead of getting the data
#         serializer = ProductSerializer(data=request.data) # this is used to serialize the data that is coming from the request.
#         #  Why does it use the same serializer as Get: because the data is coming in the same format as the data is going out so serilizer will serialize and deserialize the data at the same time
#         # INSTEAD OF THIS:
#         # if serializer.is_valid():
#         #     serializer.validate() # the data is gonna be available in the serializer.validate()
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # WE CAN USE THIS:
#         serializer.is_valid(raise_exception=True) # checks whether the user imput is currect or not. we can overwrite it in the serializer which we did as an example using def validate
#         serializer.save() # this is used to save the data in the database
#         # serializer.validated_data # this is for accessing the validated data
#         return Response(serializer.data, status=status.HTTP_201_CREATED) # 201 is used to show that the data is created and the data is returned in the response



# @api_view(['GET', 'PUT', 'DELETE']) # put is for updating the data and its difference with patch is that it updates the whole object and patch updates the part of the object
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         # try:
#         #     product = Product.objects.get(pk=id) # get the product from the database
#         #     serializer = ProductSerializer(product) # converting the data into json format
#         #     return Response(serializer.data) # serializer.data gives you the data in dict format
#         #     # the conversion of dict to json is done hiddenly by the rest_framework and by json renderer
#         # except Product.DoesNotExist:
#         #     return Response(status=status.HTTP_404_NOT_FOUND) # if the product is not found then return 404 status code. 
#         #     # this is the standard REST API status code

#         # INSTED the same thing:
#         # product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data) # puting product in the first argument is used to update the product and data=request.data is used to update the data. 
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED) # 202 is used to show that the request is accepted and the data is updated
    
#     elif request.method == "DELETE":
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is in stock'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) # 204 is used to show that the data is deleted and no content is returned


# @api_view(["GET", "POST"])
# def collection_list(request):
#     if request.method == "GET":
#         collections = Collection.objects.annotate(products_count=Count('product')) # this is used to get the count of the products in the collection
#         serializer = CollectionSerializer(collections, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#     elif request.method == "DELETE":
#         if collection.products_count > 0:
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# # CLASS BASED VIEW ---------------- LEVEL 2 ----------------
# # it is better: 1) avoid having nested if statements
# class ProductList(APIView): # this is the same as the function based view but it is the class based view. function based is the one that we have been using till now
#     def get(self, request):
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(products, many=True, context={'request': request})
#         return Response(serializer.data) 

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# # MIXINS ---------------- LEVEL 3 ----------------
# class ProductList(ListCreateAPIView):
#     # if you dont have any logic or condition then you can use just the attributes
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     # if you want to have some logic or some condiotion then you use theses methods
#     # mayber you want to check the current user permitions and give them some filter
#     def get_queryset(self):
#         return Product.objects.all()
    
#     def get_serializer_class(self):
#         return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is in stock'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#         if collection.product.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


# ModelViewSet ---------------- LEVEL 4 ---------------- Suppurts a list of object and their specific id at the same time
# we again mix the product list and product detail view because they have a lot of same code
class ProductViewSet(ModelViewSet):  # Sometimes we only want to read only so we can use ReadOnlyModelViewSet
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # easier way to filter the data
    filterset_fields = ['collection_id', 'unit_price'] # put the filtering over here    
    search_fields = ['title', 'description'] # this is for searching and not filtering. but both use the same filter_backends
    OrderingFilter = ['unit_price', 'last_update'] # this is used to order the data accending or decending

    pagination_class = PageNumberPagination # this is used to paginate the data. it is used to show the data in pages
    # We changed the page size in the settings.py file under the rest_framework section
    # We need this if we only want this view to have pagination. if we want all the views to have pagination then we can set the pagination in the settings.py file under the rest_framework section and remove this line

    # How we can filter the data using the url parameters. meaning if we want to get the products of a specific collection. but the code up is the better way to do this
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs): # distroy is used to delete only one object 
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is in stock'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # if you dont need a fucntionality just simply dont override it
    # def delete(self, request, pk): # we use distroy instead of delete because delete would appearand delete all the products but destroy will delete only the product that is requested
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is in stock'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.prefetch_related('items__product').all() 
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self): # get Context is beasically when we want to give url parameters to the serializer
        return {'product_id': self.kwargs['product_pk']} # we do this because we want to get the product id from the url and pass it to the serializer becuase we dont want to get the product id from the user because it can be manipulated
    

class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin): # CreateModelMixin is used to create the object and GenericViewSet is used to get the object. toghether they are used to create and get the object. so we can use the post and get request. 
    queryset = Cart.objects.all() # what is the point of this queryset when it doesnt show it: it is used to get the queryset for the serializer
    serializer_class = CartSerializer

        
class CartItemViewSet(ModelViewSet):
    # serializer_class = CartItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete'] # ALLOWED FUNCTIONALITIES
    
    def get_serializer_class(self):
        if self.request.method == 'POST': # we choose a custome serializer for post
            return AddCartItemSerializer    
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product') # increase the speed
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']} # context is the additional data you want to give to serializer. and kwargs is the qrguments captured from urls




