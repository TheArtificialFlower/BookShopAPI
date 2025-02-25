from django.test import TestCase
from model_bakery import baker
from management.models import Order, OrderItems, Book, Coupons, Category
from accounts.models import User
from django.utils.timezone import now
from datetime import timedelta


class TestOrderModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="root@email.com", phone_num="09119710752", full_name="marzie", password="root")
        self.category = Category.objects.create(name="Fiction", slug="fiction")
        self.book = Book.objects.create(
            category=self.category,
            title="Test Book",
            description="This is a test book.",
            image="test.jpg",
            price=1000,
            is_available=True
        )
        self.order = Order.objects.create(user=self.user, paid=False, coupon=None)
        self.order_item = OrderItems.objects.create(
            order=self.order,
            product=self.book,
            price=self.book.price,
            quantity=2
        )


    def test_total_quantity(self):
        self.assertEqual(self.order.get_total_price(), 2000)


    def test_total_quantity_coupon(self):
        self.order.coupon = 10
        self.assertEqual(self.order.get_total_price(), 1800)

    def test_get_item_price(self):
        self.assertEqual(self.order_item.get_cost(), 2000)
