from django.test import TestCase
from django.urls import reverse
from catalog.models import Brand
import datetime

from django.utils import timezone
from django.contrib.auth.models import User # Required to assign User as a borrower

from catalog.models import FurnitureInstance, Furniture, Type


class RedirectWithoutLoginTest(TestCase):
    def test_redirect_personal_page_if_not_logged_in(self):
        response = self.client.get(reverse('my-account'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/myaccount/')

    def test_redirect_workers_page_if_not_logged_in(self):
        response = self.client.get(reverse('workers-page'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/workers_page/')


class PersonalAccountViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        test_brand = Brand.objects.create(name='Jojo', country='Japan')
        test_type = Type.objects.create(name='table')
        test_furniture = Furniture.objects.create(
            name='test Furniture',
            description='descriptiondescriptiondescription',
            isbn='description12',
            brand=test_brand,
        )

        type_objects_for_furniture = Type.objects.all()
        test_furniture.type.set(type_objects_for_furniture)
        test_furniture.save()

        number_of_furniture_instances = 30
        for furniture_copy in range(number_of_furniture_instances):
            delivery_day = timezone.localtime() + datetime.timedelta(days=furniture_copy%5)
            status = 'a'
            FurnitureInstance.objects.create(
                furniture=test_furniture,
                delivery_day=delivery_day,
                status=status,
            )

    def test_logged_in_access_to_personal_page(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-account'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/personal_account.html')

    def test_only_users_furniture_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-account'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('furnitureinstance_list' in response.context)
        self.assertEqual(len(response.context['furnitureinstance_list']), 0)

        furnitures = FurnitureInstance.objects.all()[:10]
        for furniture in furnitures:
            furniture.status = 'r'
            furniture.buyer = User.objects.get(username='testuser1')
            furniture.save()

        response = self.client.get(reverse('my-account'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('furnitureinstance_list' in response.context)

        for furnitureitem in response.context['furnitureinstance_list']:
            self.assertEqual(response.context['user'], furnitureitem.buyer)
            self.assertEqual(furnitureitem.status, 'r')

    def test_pages_ordered_by_delivery_day(self):
        for furniture in FurnitureInstance.objects.all():
            furniture.status = 'r'
            furniture.buyer = User.objects.get(username='testuser1')
            furniture.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-account'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['furnitureinstance_list']), 30)

        last_date = 0
        for furniture in response.context['furnitureinstance_list']:
            if last_date == 0:
                last_date = furniture.delivery_day
            else:
                self.assertTrue(last_date <= furniture.delivery_day)
                last_date = furniture.delivery_day





class BrandListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_brands = 13

        for brand_id in range(number_of_brands):
            Brand.objects.create(
                name=f'Jojo {brand_id}',
                country=f'Japan {brand_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/brand/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('brand'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('brand'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/brand_list.html')

    def test_pagination(self):
        response = self.client.get(reverse('brand'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['brand_list']), 8)

    def test_lists_all_brands(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('brand')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['brand_list']), 5)