from django.db import models

# Create your models here.
class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    contact_no = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    enqdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Enquiry from {self.name} - {self.subject}'
    

class LoginInfo(models.Model):
    usertype = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=10, default='active')

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    contactno = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=256)
    cpassword = models.CharField(max_length=256)
    profile = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    address=models.TextField(max_length=500, default='')
    login = models.OneToOneField(LoginInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} => {self.email}"