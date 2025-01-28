from django.contrib import admin
from .models import Category, Book, BookRating, Order, OrderItems, Coupons


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_available")
    list_filter = ("is_available", "category")
    search_fields = ("title", "category__name")
    list_editable = ("price", "is_available")


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "created")
    list_filter = ("created", "book")
    search_fields = ("user__username", "book__title")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "paid", "created", "updated", "coupon")
    list_filter = ("paid", "created", "updated")
    search_fields = ("user__username",)
    readonly_fields = ("created", "updated")


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity")
    list_filter = ("order", "product")
    search_fields = ("order__user__username", "product__title")


@admin.register(Coupons)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "is_active", "valid_from", "valid_until")
    list_filter = ("is_active", "valid_from", "valid_until")
    search_fields = ("code",)
    list_editable = ("is_active",)