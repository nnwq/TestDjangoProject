from django.db import models
from datetime import datetime

director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Director'),
    (admin, 'Manager'),
    (cook, 'Cook'),
    (cashier, 'Cashier'),
    (cleaner, 'Cleaner')
]


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=3,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.slpit()[0]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default='Composition is not indicated')


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True,)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()
        else:
            return (datetime.now() - self.time_in).total_seconds()


class ProductOrder(models.Model):
    Order = models.ForeignKey('Product', on_delete=models.CASCADE)
    Product = models.ForeignKey('Order', on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def total_amount(self):
        product_price = self.product.price
        return product_price * self.amount
