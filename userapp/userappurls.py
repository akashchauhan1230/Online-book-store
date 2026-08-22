
from django.urls import path
from . import views

urlpatterns = [
    path('userdash/',views.userdash,name='userdash'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path('addtocart<id>/',views.addtocart,name='addtocart'),
    path('removeitem<id>/',views.removeitem,name='removeitem'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment-success/',views.payment_success,name='payment_success'),
    path('userorders/',views.userorders,name='userorders'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),


    

    
    
   
]