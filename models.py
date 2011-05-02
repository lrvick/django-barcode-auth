from django.db import models

class UserBarcode(models.Model):
    user = models.ForeignKey(User, unique=True)
    barcode = models.ImageField(unique=True)

# Create your models here.
