from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.utils import timezone
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, CategorySerializer

class MenuItemsView(APIView):
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['price']
    search_fields = ['title', 'category__title']
    filterset_fields = ['category']

    def get(self, request):
        menu_items = MenuItem.objects.all()
        category = request.query_params.get('category', None)
        if category:
            menu_items = menu_items.filter(category__title=category)
        
        ordering = request.query_params.get('ordering', None)
        if ordering:
            menu_items = menu_items.order_by(ordering)
        
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(menu_items, request)
        serializer = MenuItemSerializer(paginated_items, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuItemView(APIView):
    def get(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        menu_item = get_object_or_404(MenuItem, pk=pk)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        menu_item = get_object_or_404(MenuItem, pk=pk)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_superuser:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerUsersView(APIView):
    def get(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        managers = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data.get('username'))
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response({"detail": "User added to managers"}, status=status.HTTP_201_CREATED)

class ManagerUserView(APIView):
    def delete(self, request, userId):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=userId)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return Response({"detail": "User removed from managers"})

class DeliveryCrewUsersView(APIView):
    def get(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        crew = User.objects.filter(groups__name='Delivery crew')
        serializer = UserSerializer(crew, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data.get('username'))
        crew = Group.objects.get(name='Delivery crew')
        crew.user_set.add(user)
        return Response({"detail": "User added to delivery crew"}, status=status.HTTP_201_CREATED)

class DeliveryCrewUserView(APIView):
    def delete(self, request, userId):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=userId)
        crew = Group.objects.get(name='Delivery crew')
        crew.user_set.remove(user)
        return Response({"detail": "User removed from delivery crew"})

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        menuitem = get_object_or_404(MenuItem, pk=request.data.get('menuitem_id'))
        quantity = int(request.data.get('quantity', 1))
        unit_price = menuitem.price
        price = quantity * unit_price
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': unit_price, 'price': price}
        )
        
        if not created:
            cart_item.quantity = quantity
            cart_item.price = price
            cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
        elif request.user.groups.filter(name='Delivery crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total=total,
            date=timezone.now().date()
        )

        order_items = []
        for cart_item in cart_items:
            order_items.append(OrderItem(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            ))
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orderId):
        if request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            order = get_object_or_404(Order, pk=orderId)
        elif request.user.groups.filter(name='Delivery crew').exists():
            order = get_object_or_404(Order, pk=orderId, delivery_crew=request.user)
        else:
            order = get_object_or_404(Order, pk=orderId, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, orderId):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        order = get_object_or_404(Order, pk=orderId)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            if 'delivery_crew_id' in request.data:
                delivery_crew = get_object_or_404(User, pk=request.data['delivery_crew_id'])
                if not delivery_crew.groups.filter(name='Delivery crew').exists():
                    return Response({"detail": "User is not delivery crew"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.validated_data['delivery_crew'] = delivery_crew
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, orderId):
        if request.user.groups.filter(name='Delivery crew').exists():
            order = get_object_or_404(Order, pk=orderId, delivery_crew=request.user)
            if 'status' in request.data:
                order.status = request.data['status']
                order.save()
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            return Response({"detail": "Only status can be updated"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.is_superuser or request.user.groups.filter(name='Manager').exists():
            return self.put(request, orderId)
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, orderId):
        if not (request.user.is_superuser or request.user.groups.filter(name='Manager').exists()):
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        order = get_object_or_404(Order, pk=orderId)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
