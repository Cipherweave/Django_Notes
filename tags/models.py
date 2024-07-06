from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class TaggedItemManager(models.Manager): # how custom manager works is that we can use it to create custom queries
    def get_tags_for(self, obj_type, obj_id):
        # get all the tags for a specific object
        Content_type = ContentType.objects.get_for_model(obj_type) 
        queryset = TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type=Content_type,
                object_id=obj_id
            ) 


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


class TaggedItem(models.Model):
    objects = TaggedItemManager() # this is how we use the custom manager and we can use it like this: TaggedItem.objects.get_tags_for(Product, 1)
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product, video, atricle, etc)
    # ID (1, 2, 3, etc) we need these two for the generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # ContentType is a django model 
    # that keeps track of all the models in the project and allows us to use the generic foreign key
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # this is the generic foreign key that allows us to 
    # link to any object in the project
