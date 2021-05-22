import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta


class Type(models.Model):
    """
    Model representing type of product (clothes, furniture)
    """
    name = models.CharField(max_length=200, help_text="Enter the product type")

    def __str__(self):
        return self.name


class Furniture(models.Model):
    """
        Model representing a product
    """
    name = models.CharField(max_length=200)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text="Описание продукта")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    type = models.ManyToManyField(Type, help_text="Select a type of this product")
    published = models.BooleanField(default=False, help_text="Опубликовано")
    image = models.CharField(max_length=500, help_text="Изображение продукта", null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1000.20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('furniture-detail', args=[str(self.id)])

    def display_type(self):
        return ', '.join(type.name for type in self.type.all()[:3])
    display_type.short_description = 'type'

    def get_available_amount(self):
        return self.furnitureinstance_set.filter(status='a').count()

    class Meta:
        ordering = ['brand']


class FurnitureInstance(models.Model):
    """
        Model representing a specific copy of a furniture
        """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular furniture")
    furniture = models.ForeignKey('Furniture', on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    Availability_STATUS = (
        ('a', 'В наличии'),
        ('n', 'Куплен'),
        ('r', 'Зарезервирован'),
    )

    status = models.CharField(max_length=1, choices=Availability_STATUS, blank=True, default='m', help_text='Furniture availability')
    delivery_day = models.DateField(default=date.today() + timedelta(days=10), help_text="Delivery day")

    @property
    def delivery(self):
        if self.status == 'a':
            self.delivery_day = date.today() + timedelta(days=10)
            return "привезем уже к %s!" % self.delivery_day

        if self.delivery_day < date.today():
            self.status = 'n'
            return "был доставлен %s" % self.delivery_day

        return "будет доставлен %s" % self.delivery_day #only if reserved

    class Meta:
        ordering = ["status"]
        permissions = (("worker", "Can manage catalog items (WORKER)"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s) -- %s' % (self.id, self.furniture.name, self.status)


class Brand(models.Model):
    """
    Model representing Brand.
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('brand-detail', args=[str(self.id)])

    def get_published_furniture(self):
        return self.furniture_set.filter(published='True')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.name, self.country)

    class Meta:
        ordering = ['name']
