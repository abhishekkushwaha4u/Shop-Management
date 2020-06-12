from django.db import models
import uuid
from custom_user.models import User

product_types = (
    ('Grocery', 'Grocery'),
    ('Vegetables', 'Vegetables'),
    ('Household', 'Household'),
    ('Kids', 'Kids')
)

order_status_choices = (
    ('Created', 'Created'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)
class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=30, choices=product_types)
    code = models.CharField(max_length=10, unique=True)
    price = models.FloatField(default=0.0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_on']


class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, default='Created')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

class OrderItems(models.Model):
    order_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_fixed_item = models.FloatField(default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
