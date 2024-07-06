from itertools import count
from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models # import the models from the current directory
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count


# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10', 'Low')
        ]  
    
    def queryset(self, request: Any, queryset: QuerySet) -> QuerySet:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        return queryset


# # GENERIC TABULAR INLINE (EDITING CHILD MODELS) ------------------------------- (
# class TagInline(GenericTabularInline):
#     model = TaggedItem
#     autocomplete_fields = ['tag']
#     extra = 1
#     min_num = 1
#     max_num = 5
# # )  # we dont need this anymore because we are going to make another app (store_custom) that will make the tags app pluggable


@admin.register(models.Product) # this is how we can register the model to the admin site
class ProductAdmin(admin.ModelAdmin):
    # CREATE A CUSTOM ACTION ------------------------- (
    actions = ['clear_inventory'] # this is how we can add the custom action to the admin site
    # ) 
    search_fields = ['title__istartswith'] # this is how we can search for the product by title

    # CUSTOMIZING FORMS ------------------------------- ( check out the add product 
    # exclude = ['promotions'] 
    # readonly_fields = ['title'] # this is how we can make a field read only
    prepopulated_fields = {
        'slug': ['title'] # this is how we can make the slug field automatically populate with the title field getting filled
    }
    autocomplete_fields = ['collection'] # how we can make the collection field an autocomplete field and give it a search bar
    # )

    # # GENERIC TABULAR INLINE (EDITING CHILD MODELS) ------------------------------- (
    # inlines = [TagInline] # this is how we can edit the child model in the parent model
    # # ) 
        

    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title'] # this is how we can customize the product in the admin site
    list_editable = ['unit_price'] # this is how we can edit the unit price in the admin site
    list_per_page = 10
    list_select_related = ['collection'] # this is important because it will reduce the number of queries that are made to the database
    list_filter = ['collection', 'last_update', InventoryFilter] # this is how we can filter the products by collection

    def collection_title(self, product): # sometimes we need to access the related model fields this is how we can do it. we could also just call the collection but this is how we can take a specific field from the collection
        return product.collection.title  # however this is not the best way to do it because it will make a query to the database for each product. so we use list_select_related to reduce the number of queries

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    # CREATE A CUSTOM ACTION ------------------------- (
    @admin.action(description='Clear inventory') # this is how we can create a custom action in the admin site
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )
    # ) -----------------------------------------------


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # CUSTOMIZING FORMS ------------------------------- ( 
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] 
    # )
    list_display = ['first_name', 'last_name', 'membership', 'customer_order_count']
    list_editable = ['membership']
    list_per_page = 10 
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith'] # this is how we can search for the customer by first name and last name

    def customer_order_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, customer.customer_order_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.annotate(customer_order_count=Count('order'))

# EDITING CHILD MODELS ------------------------------- (
class OrderItemInline(admin.TabularInline): # this is how we can edit the child model in the parent model
    model = models.OrderItem
    autocomplete_fields = ['product'] # this is how we can make the product field an autocomplete field and give it a search bar
    extra = 0  # this is how we can remove the extra fields that are added by default you can comment this out to see the difference
    min_num = 1  # this is how we can set the minimum number of fields that are required
    max_num = 10  # basicly howm many fields (items) can be added
# )
   

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # CUSTOMIZING FORMS ------------------------------- ( 
    autocomplete_fields = ['customer'] 
    # )
    # EDITING CHILD MODELS ------------------------------- (
    inlines = [OrderItemInline]   # we have to set the inlines to the child model that we want to edit
    # )
    list_display = ['id', 'placed_at', 'customer_name']
    list_per_page = 10 
    list_select_related = ['customer']

    def customer_name(self, order):
        return f"{order.customer.first_name} {order.customer.last_name}"
    
    


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    # CUSTOMIZING FORMS ------------------------------- ( check out the add product
    search_fields = ['title__istartswith']   # we put this to clearify when this object is searched, what attribute should be used for searching. in this case we are using the title
    # )

    @admin.display(ordering='product_count')
    def products_count(self, collection): # this is how we can create a link to the product page in the admin site
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })) # this is basically creating a url that will take us to the product page with the collection id as a filter.
        # even if you put the ?collection__id=1 in the url it will still work because django will automatically convert it to a query string
        
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(product_count=Count('product'))
    


# this is how we register the models to the admin site
# admin.site.register(models.Collection)
# admin.site.register(models.Product) # so this is not needed anymore
# admin.site.register(models.Customer)
# admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Address)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Promotion)