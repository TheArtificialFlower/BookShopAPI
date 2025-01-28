from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, \
    CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response
from .models import Category, Book, BookRating, Order, OrderItems, Coupons
from .serializers import BookSerializer, CartSerializer, OrderSerializer, CouponSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .cart import Cart
from permissions import CartPermissions
from utils import cart_add
from rest_framework.pagination import PageNumberPagination


class BookManagementView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsAdminUser,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BookSerializer



class BookCreateView(CreateAPIView):
    model = Book
    permission_classes = (IsAdminUser,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BookSerializer



class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    # Checks if user asked for a category
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug', None)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = Book.objects.filter(category=category)
        return queryset



class BookDetailsView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_object(self):
        category_slug = self.kwargs.get('category_slug', None)
        book_pk = self.kwargs.get('pk', None)
        category = get_object_or_404(Category, slug=category_slug)
        book = get_object_or_404(Book, category=category, pk=book_pk)
        return book


    def patch(self, request, *args, **kwargs):
        book = self.get_object()
        like = BookRating.objects.filter(book=book, user=request.user)
        if not request.user.is_authenticated:
            return Response({"message": "Please login first."}, status=status.HTTP_401_UNAUTHORIZED)

        like.delete() if like else BookRating.objects.create(book=book, user=request.user)
        return Response(BookSerializer(book).data)


    def post(self, request, *args, **kwargs):
        book = self.get_object()
        cart = cart_add(request, book)
        return Response(data=cart.data, status=status.HTTP_201_CREATED)



class CartView(APIView):
    """
    CartView provides API endpoints to interact with a user's cart and manage their orders.
    This class contains the following methods:
    - `get`: Retrieve and return the current state of the cart with serialized data.
    - `post`: Create a new order based on the current cart contents. Clears the cart after successful order creation.
    - `delete`: Remove a specific item from the cart or clear the entire cart. Supports item-specific deletion via `pk`.
    """
    permission_classes = (CartPermissions,)

    def get(self, request, pk=None):
        cart = Cart(request)
        cart_data = cart.get_data(cart)
        serializer = CartSerializer(data=cart_data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        cart = Cart(request)
        cart_data = cart.get_data(cart)
        if cart_data["items"]:
            Order.objects.filter(user=request.user).delete() # Checks and deletes existing order
            order = Order.objects.create(user=request.user)
            for item in cart_data["items"]:
                book = item["book"]
                OrderItems.objects.create(
                    order=order,
                    product=item["instance"],
                    price=book["price"],
                    quantity=item["quantity"]
                )
            cart.clear()
            return Response("Order added successfully...", status=status.HTTP_201_CREATED)
        return Response({"message": "Your cart is empty..."}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        cart = Cart(request)
        if pk is not None:
            book = get_object_or_404(Book, pk=pk)
            cart.delete(book.id)
        else:
            cart.clear()
        cart_data = cart.get_data(cart)
        serializer = CartSerializer(data=cart_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class OrderView(RetrieveUpdateDestroyAPIView):
    """
    OrderView provides API endpoints for retrieving, updating, and deleting a user's order.
    This class supports the following operations:
    - `retrieve`: Retrieve the details of the user's current order. Returns an error message if no order exists.
    - `update`: Apply a coupon code to the user's current order, updating the order's discount. Returns an error if the order or coupon is invalid.
    - `destroy`: Delete the user's current order. Returns an error if no order exists.
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


    def retrieve(self, request, *args, **kwargs):
        order = self.get_queryset().first()
        if order:
            return Response(self.serializer_class(order).data)
        return Response({"message": "You have not ordered anything yet...check your cart."},
                        status=status.HTTP_404_NOT_FOUND)


    def update(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user).first()
        if not order:
            return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            coupon_code = serializer.validated_data["code"]
            coupon = Coupons.objects.get(code=coupon_code)
            order.coupon = coupon.discount
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        order = self.get_queryset().first()
        if order:
            order.delete()
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)