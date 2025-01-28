from django.urls import path, include
from . import views

urlpatterns = [
    path("books/", views.BookListView.as_view()),
    path("books/<slug:category_slug>/", views.BookListView.as_view()),
    path("books/<slug:category_slug>/<int:pk>/", views.BookDetailsView.as_view()),
    path("cart/", views.CartView.as_view()),
    path("cart/<int:pk>/", views.CartView.as_view()),
    path("order/", views.OrderView.as_view()),
    path('manage/create/', views.BookCreateView.as_view()),
    path('manage/<int:pk>/', views.BookManagementView.as_view()),
]
