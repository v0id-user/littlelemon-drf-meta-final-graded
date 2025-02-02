# Final Project Django API

This is a Django API for the Little Lemon restaurant.


# Project Requirements

## API Endpoints

### User Registration and Authentication
- [ ] POST `/api/users` - Create new user
- [ ] GET `/api/users/users/me/` - Get current user details 
- [ ] POST `/token/login/` - Generate access token

### Menu Items
#### Customer/Delivery Crew Access
- [ ] GET `/api/menu-items` - List all menu items
- [ ] GET `/api/menu-items/{menuItem}` - Get single menu item
- [ ] Block POST/PUT/PATCH/DELETE access

#### Manager Access  
- [ ] GET `/api/menu-items` - List all menu items
- [ ] POST `/api/menu-items` - Create menu item
- [ ] GET `/api/menu-items/{menuItem}` - Get single menu item
- [ ] PUT/PATCH `/api/menu-items/{menuItem}` - Update menu item
- [ ] DELETE `/api/menu-items/{menuItem}` - Delete menu item

### User Group Management (Managers Only)
#### Manager Users
- [ ] GET `/api/groups/manager/users` - List all managers
- [ ] POST `/api/groups/manager/users` - Assign user as manager
- [ ] DELETE `/api/groups/manager/users/{userId}` - Remove manager role

#### Delivery Crew Users
- [ ] GET `/api/groups/delivery-crew/users` - List delivery crew
- [ ] POST `/api/groups/delivery-crew/users` - Assign user as delivery crew
- [ ] DELETE `/api/groups/delivery-crew/users/{userId}` - Remove delivery crew role

### Cart Management (Customers Only)
- [ ] GET `/api/cart/menu-items` - View cart items
- [ ] POST `/api/cart/menu-items` - Add item to cart
- [ ] DELETE `/api/cart/menu-items` - Clear cart

### Order Management
#### Customer Access
- [ ] GET `/api/orders` - List user's orders
- [ ] POST `/api/orders` - Create order from cart
- [ ] GET `/api/orders/{orderId}` - Get order details

#### Manager Access
- [ ] GET `/api/orders` - List all orders
- [ ] PUT/PATCH `/api/orders/{orderId}` - Update order/assign crew
- [ ] DELETE `/api/orders/{orderId}` - Delete order

#### Delivery Crew Access
- [ ] GET `/api/orders` - List assigned orders
- [ ] PATCH `/api/orders/{orderId}` - Update delivery status

## Additional Requirements

### User Groups
- [ ] Create Manager group
- [ ] Create Delivery Crew group
- [ ] Set up customer as default role

### Error Handling
- [ ] 200 OK - Successful GET/PUT/PATCH/DELETE
- [ ] 201 Created - Successful POST
- [ ] 403 Unauthorized - Failed authorization
- [ ] 401 Forbidden - Failed authentication
- [ ] 400 Bad Request - Invalid data
- [ ] 404 Not Found - Resource doesn't exist

### API Features
- [ ] Implement filtering for menu items and orders
- [ ] Add pagination for menu items and orders
- [ ] Add sorting capabilities for menu items and orders
- [ ] Set up throttling for authenticated users
- [ ] Set up throttling for anonymous users
