import random
from django.core.management.base import BaseCommand
from shop.models import User, Product, Order, OrderItem

class Command(BaseCommand):
    help = "Generate sample orders for testing"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        products = list(Product.objects.all())  # Retrieve all products

        for _ in range(1000):
            user = random.choice(users)

            name = f"Customer {user.username}"
            phone = f"09{random.randint(10000000, 99999999)}"
            address = f"Random Address {random.randint(1, 100)}"
            note = "This is a sample note."
            payment_method = random.choice(['COD', 'MoMo'])
            status = random.choice(['Pending', 'Shipping', 'Delivered', 'Cancelled'])

            order = Order.objects.create(
                user=user,
                name=name,
                phone=phone,
                address=address,
                note=note,
                payment_method=payment_method,
                status=status,
            )

            for _ in range(random.randint(3, 6)):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                price = product.get_current_price()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    size=None,  # Assuming no specific size
                    quantity=quantity,
                    price=price,
                )
        self.stdout.write(self.style.SUCCESS("Sample orders created successfully!"))