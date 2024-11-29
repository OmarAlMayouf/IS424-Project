from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    picture = models.URLField(null=True)
    def __str__(self):
        return self.name
class PharmacyInstance(models.Model):
    names = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=10,primary_key=True)
    password = models.CharField(max_length=128) 
    def __str__(self):
        return self.phonenumber