from django.urls import path, include
from . import views


managementpatterns = [
    path('books/create/', views.BookCreateView.as_view()),
    path('books/<int:pk>/', views.BookManagementView.as_view()),
    path('orders/', views.OrderManagementView.as_view()),
    path('orders/<int:pk>/', views.OrderUpdateManagementView.as_view())
]


urlpatterns = [
    path("books/", views.BookListView.as_view()),
    path("books/<slug:category_slug>/", views.BookListView.as_view()),
    path("books/<slug:category_slug>/<int:pk>/", views.BookDetailsView.as_view()),
    path("cart/", views.CartView.as_view()),
    path("cart/<int:pk>/", views.CartView.as_view()),
    path("order/", views.OrderView.as_view()),
    path('manage/', include(managementpatterns))
]
