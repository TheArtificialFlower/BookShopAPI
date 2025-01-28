from .models import Book

SESSION_CART_ID = "cart"


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_CART_ID)
        if cart is None:
            cart = self.session[SESSION_CART_ID] = {}
        self.cart = cart


    def save(self):
        self.session.modified = True


    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart.keys():
            if self.cart[product_id]["quantity"] > 1:
                self.cart[product_id]["quantity"] -= 1
                self.save()
            else:
                del self.cart[product_id]
                self.save()

    def items(self):
        for book_id, details in self.cart.items():
            book = Book.objects.get(id=book_id)

            yield {
                'book': book,
                'quantity': details['quantity'],
                'price': float(details['price']),
                'total_price': float(details['price']) * details['quantity'],
            }


    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def get_total_price(self):
        return sum(int(item["price"]) * item["quantity"] for item in self.cart.values())

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session[SESSION_CART_ID]
        self.save()

    def get_data(self, cart):
        cart_data = {
            "items": [
                {
                    "book": {
                        "id": item['book'].id,
                        "title": item['book'].title,
                        "image": item['book'].image.url,
                        "price": item['book'].price
                    },
                    "quantity": item['quantity'],
                    "instance": Book.objects.get(id=item['book'].id)
                }
                for item in cart.items()
            ],
            "total_price": cart.get_total_price(),
            "total_quantity": cart.get_total_quantity(),
        }
        return cart_data


