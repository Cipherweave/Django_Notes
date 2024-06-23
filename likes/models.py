from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class LikedItem(models.Model):
    # what user like what item
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Type (product, video, atricle, etc)
    # ID (1, 2, 3, etc) we need these two for the generic foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # specifies which type of object is being liked (e.g., Product, Video).
    # that keeps track of all the models in the project and allows us to use the generic foreign key
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  # this is the generic foreign key that allows us to 
    # link to any object in the project