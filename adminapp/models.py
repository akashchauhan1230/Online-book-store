from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField()
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()
    language = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='books/',blank=True, null=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title