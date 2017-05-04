from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get("/inscricao/")

    def test_get_code(self):
        """ GET /inscricao /should return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Deve usar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_html(self):
        """html da resposta deve conter input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6) # 4 campos, 1 botão e a csrf
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"', 1)
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """html deve conter tag de proteção contra csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context deve ter SubscriptionForm"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form deve ter 4 campos"""
        form = self.resp.context["form"]
        self.assertSequenceEqual(['name','cpf','email','phone'],list(form.fields))