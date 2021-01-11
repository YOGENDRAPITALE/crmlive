from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerPage , name="register"),
    path('login/',views.loginPage , name="login"),
    path('logout/',views.logoutUser , name="logout"),
    path('user/',views.userPage , name="user"),
    path('account/',views.accountSettings , name="account"),

    path('',views.home , name="home"),
    path('product/',views.product, name="product"),
    path('customer/<str:cid>/',views.customer, name="customer"),
    
    path('create_order/<str:coid>/',views.create_order, name="create_order"),
    path('update_order/<str:uoid>/',views.update_order, name="update_order"),
    path('delete_order/<str:doid>/',views.delete_order, name="delete_order"),
    
    path('create_customer/',views.create_customer, name="create_customer"),
    path('update_customer/<str:ucid>/',views.update_customer, name="update_customer"),
    path('delete_customer/<str:dcid>/',views.delete_customer, name="delete_customer"),

]	
	