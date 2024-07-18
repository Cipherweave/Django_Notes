from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views


# # URLConf   -------------- LEVEL 1, 2 --------------
# urlpatterns = [
#     path('products/', views.ProductList.as_view()), # as_view() is used to convert the class into the view
#     path('products/<int:pk>/', views.ProductDetail.as_view()), # <int: id> is a path converter that will get the value from the url and pass it to the view it make sure that the value is an integer
#     path('collections/<int:pk>/', views.CollectionDetail.as_view()), # name is used to give the name to the url so that we can use it in the serializer,
#     path('collections/', views.CollectionList.as_view()),
# ]


# URLConf   -------------- LEVEL 3 --------------
# router = DefaultRouter() # routers is used to create the urls for the viewset. this process is called as url routing
# # DefaultRouter had two extra functionalities more than SimpleRouter: you can get a .json response and you can get a .api response 
# router.register('products', views.ProductViewSet) # this is used to register the viewset with the router
# router.register('collections', views.CollectionViewSet) # this is used to register the viewset with the router

# # urlpatterns = router.urls # this is used to get the urls from the router
# # OR
# urlpatterns = [
#     path('', include(router.urls)) # this is used to include the urls from the router. this way you can include other urls as well
# ]


# NESTED ROUTING  -------------- LEVEL 3.2 --------------
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products') # this is used to register the viewset with the router
router.register('collections', views.CollectionViewSet) # this is used to register the viewset with the router

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product') # this is used to create a nested router.
# lookup is basically the name of the field that is used to get the value from the url. in this case it is product

product_router.register('reviews', views.ReviewViewSet, basename='product-reviews') # this is used to register the viewset with the router
# BASE NAME is used to give the name to the url so that we can use it in the serializer. by default it is the queryset name in lowercase

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(product_router.urls)),
# ]
# or 
urlpatterns = router.urls + product_router.urls # this is used to include the urls from the router. 