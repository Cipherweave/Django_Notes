from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()), # as_view() is used to convert the class into the view
    path('products/<int:id>/', views.ProductDetail.as_view()), # <int: id> is a path converter that will get the value from the url and pass it to the view it make sure that the value is an integer
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail'), # name is used to give the name to the url so that we can use it in the serializer,
    path('collections/', views.CollectionList.as_view()),
]
