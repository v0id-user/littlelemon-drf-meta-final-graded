from django.urls import path
from .views import *

urlpatterns = [
    path('api/menu-items', MenuItemsView.as_view()),
    path('api/menu-items/<int:pk>', MenuItemView.as_view()),
    path('api/categories', CategoryView.as_view()),
    path('api/groups/manager/users', ManagerUsersView.as_view()),
    path('api/groups/manager/users/<int:userId>', ManagerUserView.as_view()),
    path('api/groups/delivery-crew/users', DeliveryCrewUsersView.as_view()),
    path('api/groups/delivery-crew/users/<int:userId>', DeliveryCrewUserView.as_view()),
    path('api/cart/menu-items', CartView.as_view()),
    path('api/orders', OrdersView.as_view()),
    path('api/orders/<int:orderId>', OrderView.as_view()),
]