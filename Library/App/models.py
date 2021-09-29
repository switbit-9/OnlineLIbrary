from datetime import datetime, timezone
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import EmailField, NullBooleanField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)
    points = models.IntegerField(default=0)
    adress = models.CharField(max_length=200)
    user_img = models.ImageField(upload_to='uploads/profile pictures', null= True, blank= True)  
  

    def __str__(self):
        return self.username

class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    adress = models.CharField(max_length=100, blank= True )
    bio = models.CharField(max_length=200, blank= True)
    author_img = models.URLField(max_length=2000, default='https://upload.wikimedia.org/wikipedia/commons/e/e4/Whitescreen.jpg')
    url_a = models.URLField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name


class Books(models.Model):
    categories = [
        ('1', 'Fiction'),
        ('2', 'Romantic'),
        ('3', 'Action'),
        ('4', 'Phylosofic'),
    ]
    
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    availability = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    books_img = models.URLField(max_length=2000, default=None, blank=True, null=True )
    publisher = models.ForeignKey(Publisher ,on_delete=models.CASCADE, null=True, blank=True, default=None)
    category = models.CharField(max_length=20, choices=categories, blank=True)
    user_id = models.ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    content = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.title



class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    book = models.ForeignKey(Books, on_delete=CASCADE, null=True, blank=True)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.date)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    books = models.ForeignKey(Books, on_delete=CASCADE)
    content = models.CharField(max_length=100)
    rating = models.IntegerField()

    def __str__(self):
        return self.content

class Message(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Save(models.Model):
    user= models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Books, on_delete=CASCADE)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.id

class AddBook(models.Model):
    pass

class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Books, on_delete=CASCADE)

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    saved = models.ForeignKey(Save, on_delete=CASCADE)
    borrowed = models.ForeignKey(Borrow, on_delete=CASCADE)
