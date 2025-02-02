# Final Project Django API

This is my implementation of the Project Requirements for the final Little Lemon API project using Django Rest Framework (DRF) as part of the APIs course from Meta.

# Project Requirements

## API Endpoints

### User Registration and Authentication
- [x] POST `/api/users` - Create new user
- [x] GET `/api/users/users/me/` - Get current user details 
- [x] POST `/token/login/` - Generate access token

### Menu Items
#### Customer/Delivery Crew Access
- [x] GET `/api/menu-items` - List all menu items
- [x] GET `/api/menu-items/{menuItem}` - Get single menu item
- [x] Block POST/PUT/PATCH/DELETE access

#### Manager Access  
- [x] GET `/api/menu-items` - List all menu items
- [x] POST `/api/menu-items` - Create menu item
- [x] GET `/api/menu-items/{menuItem}` - Get single menu item
- [x] PUT/PATCH `/api/menu-items/{menuItem}` - Update menu item
- [x] DELETE `/api/menu-items/{menuItem}` - Delete menu item

### User Group Management (Managers Only)
#### Manager Users
- [x] GET `/api/groups/manager/users` - List all managers
- [x] POST `/api/groups/manager/users` - Assign user as manager
- [x] DELETE `/api/groups/manager/users/{userId}` - Remove manager role

#### Delivery Crew Users
- [x] GET `/api/groups/delivery-crew/users` - List delivery crew
- [x] POST `/api/groups/delivery-crew/users` - Assign user as delivery crew
- [x] DELETE `/api/groups/delivery-crew/users/{userId}` - Remove delivery crew role

### Cart Management (Customers Only)
- [x] GET `/api/cart/menu-items` - View cart items
- [x] POST `/api/cart/menu-items` - Add item to cart
- [x] DELETE `/api/cart/menu-items` - Clear cart

### Order Management
#### Customer Access
- [x] GET `/api/orders` - List user's orders
- [x] POST `/api/orders` - Create order from cart
- [x] GET `/api/orders/{orderId}` - Get order details

#### Manager Access
- [x] GET `/api/orders` - List all orders
- [x] PUT/PATCH `/api/orders/{orderId}` - Update order/assign crew
- [x] DELETE `/api/orders/{orderId}` - Delete order

#### Delivery Crew Access
- [x] GET `/api/orders` - List assigned orders
- [x] PATCH `/api/orders/{orderId}` - Update delivery status

## Additional Requirements

### User Groups
- [x] Create Manager group
- [x] Create Delivery Crew group
- [x] Set up customer as default role

### Error Handling
- [x] 200 OK - Successful GET/PUT/PATCH/DELETE
- [x] 201 Created - Successful POST
- [x] 403 Unauthorized - Failed authorization
- [x] 401 Forbidden - Failed authentication
- [x] 400 Bad Request - Invalid data
- [x] 404 Not Found - Resource doesn't exist

### API Features
- [x] Implement filtering for menu items and orders
- [x] Add pagination for menu items and orders
- [x] Add sorting capabilities for menu items and orders
- [x] Set up throttling for authenticated users
- [x] Set up throttling for anonymous users
