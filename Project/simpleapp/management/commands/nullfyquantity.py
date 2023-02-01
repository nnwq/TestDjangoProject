from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product

class Command(BaseCommand):
    help = 'Deletes all products'

    def handle(self, *args, **options):
        for product in Products.objects.all():
            product.quantity = 0
            product.save()

            self.stdout.write(self.style.SUCCESS("Successfully nulled product '%s'' " % str(product)))
