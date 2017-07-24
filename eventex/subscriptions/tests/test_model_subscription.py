from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(
            name = 'Henrique Basros',
            cpf = '12345678901',
            email= 'henrique@bastos.net',
            phone= '21-99999-7777'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription deve ter o atributo created_at"""
        self.assertIsInstance(self.obj.created_at, datetime)