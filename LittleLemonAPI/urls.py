from django.urls import path
from . import views

urlpatterns = [
    path('api/menu-items', views.MenuItemsView.as_view()),
    path('api/menu-items/<int:pk>', views.MenuItemView.as_view()),
    path('api/categories', views.CategoryView.as_view()),
    path('api/groups/manager/users', views.ManagerUsersView.as_view()),
    path('api/groups/manager/users/<int:userId>', views.ManagerUserView.as_view()),
    path('api/groups/delivery-crew/users', views.DeliveryCrewUsersView.as_view()),
    path('api/groups/delivery-crew/users/<int:userId>', views.DeliveryCrewUserView.as_view()),
    path('api/cart/menu-items', views.CartView.as_view()),
    path('api/orders', views.OrdersView.as_view()),
    path('api/orders/<int:orderId>', views.OrderView.as_view()),
]