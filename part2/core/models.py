from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):   # we make this model to inherite the built in Auth Abstract user. We do this make the email unique.
    email = models.EmailField(unique=True)  # Remember, User Auth model is different from the cutomer model we made.
    