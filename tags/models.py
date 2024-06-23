from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product, video, atricle, etc)
    # ID (1, 2, 3, etc) we need these two for the generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # ContentType is a django model 
    # that keeps track of all the models in the project and allows us to use the generic foreign key
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # this is the generic foreign key that allows us to 
    # link to any object in the project
