from accounts.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)


    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="books")
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=999)
    image = models.ImageField(upload_to="media/")
    price = models.PositiveBigIntegerField(validators=[MinValueValidator(0),])
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="likes")
    created = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ("paid", "-updated")

    def __str__(self):
        return f"{self.user} --- {self.paid}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            total = total - ((self.coupon / 100) * total)
        return int(total)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity




class Coupons(models.Model):
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    discount = models.IntegerField(validators=[MaxValueValidator(99),MinValueValidator(1)])
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code

