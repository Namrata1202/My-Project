from django.db import models
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class BookUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    college = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.user.username

class   Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    book_categories = models.ForeignKey( Categories,on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=100)
    image =models.ImageField(upload_to="img/%y",null=True)
    

    def __str__(self):
        return self.title    

class Product(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    image =models.ImageField(upload_to="img/%y")


class MyBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_user = models.ForeignKey(BookUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title        
    

    

    
        