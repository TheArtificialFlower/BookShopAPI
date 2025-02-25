from django.test import TestCase
from management.serializers import CouponSerializer
from django.utils.timezone import now
from management.models import Coupons
from datetime import timedelta


class TestSerializerMethods(TestCase):

    def setUp(self):
        coupon = Coupons.objects.create(discount = 33, code="ABC", valid_from=now(), valid_until=now() + timedelta(minutes=2), is_active=True)

    def test_coupon_validation(self):
        serializer = CouponSerializer(data={"code":"ABC"})
        self.assertEqual(serializer.is_valid(), True)

    def test_coupon_invalidation(self):
        serializer = CouponSerializer(data={"code": "12334"})
        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("code", serializer.errors)
