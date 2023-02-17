from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from advertising.models import Advertising
from advertising.tests.factories import (
    AdvertisingFactory,
    UserFactory, ADVERTISING_STATUS,
)


class AdvertisingTest(APITestCase):
    def setUp(self) -> None:
        self.advertisings = AdvertisingFactory.create_batch(5)
        self.user = UserFactory.create()
        self.token = self.client.post(
            reverse('sign_in'),
            {
                'email': self.user.email,
                'password': 'adminadmin123'
            }
        ).data.get('access')

    def test_advertising_publish(self):
        url = reverse('advertising-create')
        expected_data = {
            "title": "test title 1",
            "description": "test description",
            "category": f"{self.advertisings[0].category.id}"
        }
        response = self.client.post(url, expected_data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = response.data
        self.assertEqual(data['title'], expected_data['title'])
        self.assertEqual(data['description'], expected_data['description'])
        self.assertEqual(str(data['category']), expected_data['category'])

    def test_change_status(self):
        ad = self.advertisings[0]
        ad.status = ''
        ad.save()
        url = reverse('change-status')
        expected_data = {
            "ids": [self.advertisings[0].id],
            "status": f"{ADVERTISING_STATUS[0]}"
        }
        response = self.client.post(url,
                                    expected_data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = response.data
        self.assertEqual(data[0]['status'], expected_data['status'])

    def tearDown(self):
        Advertising.objects.all().delete()
        get_user_model().objects.all().delete()
