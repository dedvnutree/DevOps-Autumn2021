import uuid

from django.db import models
from django.urls import reverse


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
    description = models.TextField(max_length=1000, help_text="Enter description of the product")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    type = models.ManyToManyField(Type, help_text="Select a type of this product")

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
        ordering = ['name']


class FurnitureInstance(models.Model):
    """
        Model representing a specific copy of a furniture
        """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular furniture")
    Furniture = models.ForeignKey('Furniture', on_delete=models.SET_NULL, null=True)

    Availability_STATUS = (
        ('a', 'Available'),
        ('n', 'Not available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=Availability_STATUS, blank=True, default='m', help_text='Furniture availability')

    class Meta:
        ordering = ["id"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s) -- %s' % (self.id, self.Furniture.name, self.status)

    class Meta:
        ordering = ['status']


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

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.name, self.country)

    class Meta:
        ordering = ['name']
