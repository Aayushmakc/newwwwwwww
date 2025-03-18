from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    message=models.TextField()


class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title
    


class Item(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    image=models.ImageField(upload_to='momo_images')

    def __str__(self):
        return self.title