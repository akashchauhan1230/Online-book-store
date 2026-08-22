
from django.urls import path
from . import views

urlpatterns = [
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('viewenq/', views.viewenq, name='viewenq'),
    path('delenq/<int:id>/', views.delenq, name='delenq'),
    path('delcat/<int:id>/', views.delcat, name='delcat'),
    path('adminchangepwd/',views.adminchangepwd,name='adminchangepwd'),
    path('addcat/', views.addcat, name='addcat'),
    path('viewcat/', views.viewcat, name='viewcat'),
    path('addbook/', views.addbook, name='addbook'),
    path('viewbook/', views.viewbook, name='viewbook'),
    path('adminorder/', views.adminorder, name='adminorder'),
]