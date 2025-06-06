from django.contrib import admin
from django.urls import path
from . import views
from AppOne.views import indexpage,aboutpage,womenspage,menspage,kidspage,contactpage,signup,signin,addtocart

urlpatterns = [
   path('signup/',views.signup, name='signup'),
   path('signin/',views.signin, name='signin'),
   path('indexpage/',views.indexpage,name='indexpage'),
   path('aboutpage/',views.aboutpage,name='aboutpage'),
   path('womenspage/',views.womenspage,name='womenspage'),
   path('menspage/',views.menspage,name='menspage'),
   path('kidspage/',views.kidspage,name='kidspage'),
   path('contactpage/',views.contactpage,name='contactpage'),
   path('addtocart/',views.addtocart, name='addtocart'),
   path('checkout/', views.checkout, name='checkout'),
   path('buy-now/', views.buy_now, name='buy_now'),
   path('purchased/', views.purchased_products, name='purchased_products'),
]