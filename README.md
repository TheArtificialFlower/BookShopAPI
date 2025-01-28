# Project Title

A simple Django-based API designed for managing books, orders, user profiles, and cart functionality. This project implements JWT-based authentication and supports CRUD operations for various resources.

## Features
- **Books Management**:
  - Retrieve a list of books or details of a specific book by category.
  - Create, update, or delete book entries.
- **User Management**:
  - User registration with OTP verification.
  - Token-based authentication with refresh token support.
  - User profile management (update, retrieve, delete).
- **Cart Functionality**:
  - Add items to the cart.
  - View or remove cart items.
- **Order Management**:
  - Place and manage orders with optional coupon codes.
- **API Documentation**:
  - OpenAPI schema provided in both JSON and YAML formats.

## API Endpoints
### Books
- `GET /books/` – List all books (paginated).
- `GET /books/{category_slug}/` – Retrieve books in a specific category.
- `GET /books/{category_slug}/{id}/` – Retrieve details of a specific book.
- `POST /books/{category_slug}/{id}/` – Add a new book.
- `PATCH /books/{category_slug}/{id}/` – Update a book partially.
- `DELETE /books/{category_slug}/{id}/` – Delete a book.

### User
- `POST /user/register/` – Register a new user.
- `POST /user/register/otp/` – Verify OTP for registration.
- `POST /user/token/` – Obtain JWT tokens for authentication.
- `POST /user/token/refresh/` – Refresh JWT token.
- `GET /user/profile/` – Retrieve user profile.
- `PUT /user/profile/` – Update user profile.
- `DELETE /user/profile/` – Delete user profile.

### Cart
- `GET /cart/` – Retrieve the user's cart.
- `POST /cart/` – Add items to the cart.
- `DELETE /cart/{id}/` – Remove an item from the cart.

### Orders
- `GET /order/` – View order details.
- `PUT /order/` – Update an order.
- `DELETE /order/` – Delete an order.

## Technologies Used
- **Django**: Backend framework.
- **JWT Authentication**: Secure user authentication.
- **OpenAPI (Swagger)**: API documentation and schema generation.

