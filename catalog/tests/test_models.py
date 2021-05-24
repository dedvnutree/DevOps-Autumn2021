from django.test import TestCase

from catalog.models import Brand


class BrandModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Brand.objects.create(name='ItalicBrand', country='Italy',  description="italy")

    def test_name_label(self):
        brand = Brand.objects.get(id=1)
        field_label = brand._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_country_label(self):
        brand = Brand.objects.get(id=1)
        field_value = getattr(brand, 'country')
        self.assertEqual(field_value, 'Italy')

    def test_description_label(self):
        brand = Brand.objects.get(id=1)
        field_value = getattr(brand, 'description')
        self.assertEqual(field_value, 'italy')

    def test_name_max_length(self):
        brand = Brand.objects.get(id=1)
        max_length = brand._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        brand = Brand.objects.get(id=1)
        expected_object_name = f'{brand.name}, {brand.country}'
        self.assertEqual(str(brand), expected_object_name)

    def test_get_absolute_url(self):
        brand = Brand.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(brand.get_absolute_url(), '/catalog/brand/1')