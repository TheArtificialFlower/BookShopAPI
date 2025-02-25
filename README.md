# Bookshop API

A RESTful API for managing a bookshop. This API provides endpoints for retrieving books, managing orders, handling cart operations, and user authentication and profile management. The API follows the OpenAPI 3.0 specification.

## Overview

This API includes endpoints for:

- **Books**: List, retrieve, create, update, and partially update book records.
- **Cart**: Retrieve the current cart, create orders from the cart, and delete cart items.
- **Order**: Retrieve, update (including coupon application), partially update, and delete orders.
- **User**: Manage user profiles, register new users, and obtain/refresh JWT tokens.
- **Administration**: Manage books and orders with additional endpoints for updating and deleting records.

You can also retrieve the OpenAPI schema of the API via the `/api/schema/` endpoint.

## Authentication

This API uses JWT (JSON Web Token) authentication. To authenticate:

1. **Obtain a token:**  
   Send a POST request to `/user/token/` with your credentials to receive an access and refresh token.

2. **Refresh token:**  
   When your access token expires, refresh it by sending a POST request to `/user/token/refresh/`.

Include the JWT token in the `Authorization` header for protected endpoints, like so:  
`Authorization: Bearer <your_token>`

## Endpoints

### Schema

- **GET `/api/schema/`**  
  Retrieves the OpenAPI schema for this API.  
  *Query parameters:*  
  - `format`: Select between `json` and `yaml`  
  - `lang`: Choose the language for the schema documentation  

### Books

- **GET `/books/`**  
  Retrieves a paginated list of books.  
  *Query parameter:*  
  - `page` (optional): Page number for paginated results

- **GET `/books/{category_slug}/`**  
  Retrieves a paginated list of books for a given category.  
  *Path parameter:*  
  - `category_slug`: The slug identifier of the category  
  *Query parameter:*  
  - `page` (optional)

- **GET `/books/{category_slug}/{id}/`**  
  Retrieves a single book by category and ID.  
  *Path parameters:*  
  - `category_slug`: The category slug  
  - `id`: The book identifier

- **POST `/books/{category_slug}/{id}/`**  
  Creates a new book in the specified category.  
  *Path parameters:*  
  - `category_slug`  
  - `id`  


- **PATCH `/books/{category_slug}/{id}/`**  
  Partially updates a book.  
  *Path parameters:*  
  - `category_slug`  
  - `id`  


### Cart

- **GET `/cart/`**  
  Retrieves the current state of the user's cart.

- **POST `/cart/`**  
  Creates a new order from the current cart and clears it.

- **DELETE `/cart/`**  
  Deletes a specific item from the cart or clears the entire cart.

- **GET `/cart/{id}/`**  
  Retrieves a specific cart by its ID.  
  *Path parameter:*  
  - `id`: Cart identifier

- **POST `/cart/{id}/`**  
  Creates an order from the cart identified by the provided ID.  
  *Path parameter:*  
  - `id`

- **DELETE `/cart/{id}/`**  
  Deletes the cart or specific items from it.  
  *Path parameter:*  
  - `id`

### Administration

#### Books Management

- **GET `/manage/books/{id}/`**  
  Retrieves details of a book for management purposes.  
  *Path parameter:*  
  - `id`: Book identifier

- **PUT `/manage/books/{id}/`**  
  Updates a book record completely.  
  *Path parameter:*  
  - `id`

- **PATCH `/manage/books/{id}/`**  
  Partially updates a book record.  
  *Path parameter:*  
  - `id`

- **DELETE `/manage/books/{id}/`**  
  Deletes a book record.  
  *Path parameter:*  
  - `id`

- **POST `/manage/books/create/`**  
  Creates a new book record for management.

#### Orders Management

- **GET `/manage/orders/`**  
  Retrieves a paginated list of all orders.  
  *Query parameters:*  
  - `page` (optional): Page number  
  - `search` (optional): Filter orders by user full name  
  - `order-by` (optional): Field to order results

- **GET `/manage/orders/{id}/`**  
  Retrieves details of a specific order.  
  *Path parameter:*  
  - `id`: Order identifier

- **PUT `/manage/orders/{id}/`**  
  Updates an order completely.  
  *Path parameter:*  
  - `id`

- **PATCH `/manage/orders/{id}/`**  
  Partially updates an order.  
  *Path parameter:*  
  - `id`

- **DELETE `/manage/orders/{id}/`**  
  Deletes a specific order.  
  *Path parameter:*  
  - `id`

### Order

- **GET `/order/`**  
  Retrieves details of the current user's order.

- **PUT `/order/`**  
  Updates the user's current order, for example to apply a coupon code.

- **PATCH `/order/`**  
  Partially updates the user's order.

- **DELETE `/order/`**  
  Deletes the current user's order.

### User

- **GET `/user/profile/`**  
  Retrieves the current user's profile.

- **PUT `/user/profile/`**  
  Updates the user's profile.

- **PATCH `/user/profile/`**  
  Partially updates the user's profile.

- **DELETE `/user/profile/`**  
  Deletes the user's profile.

- **POST `/user/register/`**  
  Registers a new user.  


- **POST `/user/register/otp/`**  
  Sends an OTP for user registration.  
  *Request Body:* Otp object

- **POST `/user/token/`**  
  Authenticates a user and returns JWT tokens.  
  *Request Body:* TokenObtainPair object

- **POST `/user/token/refresh/`**  
  Refreshes the JWT access token.  
  *Request Body:* TokenRefresh object

