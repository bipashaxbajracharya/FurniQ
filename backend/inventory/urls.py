from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user, name='user'),
    path('', views.home, name='home'), #customer homepage
    path('list/', views.product_list, name='product_list'), # for staffs
 
    path('login/', views.user, name='user'),
    path('register/', views.register, name='register'),
    path('logout/', views.signout, name='logout'),
    
    path('bedroom/', views.bedroom, name='bedroom'),
    path('livingroom/', views.livingroom, name='livingroom'),
    path('dining/', views.dining, name='dining'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search_results, name='search_results'),
    path('update-stock/<int:product_id>/', views.update_stock, name='update_stock'),
    path('place-order/',views.place_order, name='place_order'),
    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
]
