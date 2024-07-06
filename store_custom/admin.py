from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem

# Register your models here.

# GENERIC TABULAR INLINE (EDITING CHILD MODELS) ------------------------------- (
class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 1
    min_num = 1
    max_num = 5
# ) 


# EXTENDING THE PLUCGABLE APPS ------------------------------- (
class CustomProductAdmin(ProductAdmin):
    inlines = [
        TagInline
    ]
# )

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin) # the reason we are doing this is because we are extending the ProductAdmin class and we need