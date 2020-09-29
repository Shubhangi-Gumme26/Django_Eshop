from django.db import models
from django.db.models import CASCADE
from store.models.product import Product
from store.models.customer import Customer


class Order(models.Model):
    product = models.ForeignKey(to=Product, on_delete=CASCADE)
    customer = models.ForeignKey(to=Customer, on_delete=CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=50, default='')
    ordered_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    class Meta:
        ordering = ['-ordered_date']
