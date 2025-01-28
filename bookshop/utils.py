from management.serializers import CartSerializer
from management.cart import Cart
from django.core.mail import send_mail

EMAIL_INSTANCE = ["projectspacedevs@gmail.com",]

def cart_add(request, book):
    cart = Cart(request)
    cart.add(book, 1)
    cart_data = cart.get_data(cart)
    serializer = CartSerializer(data=cart_data)
    serializer.is_valid(raise_exception=True)
    return serializer


def send_otp_email(email,code):
    send_mail(subject="YOUR VERIFICATION CODE", message=f"code: {code}", from_email=EMAIL_INSTANCE[0], recipient_list=[email,])
