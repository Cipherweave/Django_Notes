from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),  
    path('products/<int:id>/', views.product_detail), # <int: id> is a path converter that will get the value from the url and pass it to the view it make sure that the value is an integer
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail') # name is used to give the name to the url so that we can use it in the serializer,
]
