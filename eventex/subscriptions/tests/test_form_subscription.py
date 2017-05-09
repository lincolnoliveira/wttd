from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        # self.form = self.resp.context["form"]
        self.form = SubscriptionForm()


    def test_form_has_fields(self):
        """Form deve ter 4 campos"""
        self.assertSequenceEqual(['name' ,'cpf' ,'email' ,'phone'] ,list(self.form.fields))
