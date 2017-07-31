from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
# cada classe dessa é um cenário de testes
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
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
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"',1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """html deve conter tag de proteção contra csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context deve ter SubscriptionForm"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        dados = dict(name = "João Balalão",
                     cpf = '888777666-55',
                     email = 'lincoln@cmc.pr.gov.br',
                     phone = '(41)3350-5813')
        self.resp = self.client.post('/inscricao/', dados)

    def test_post(self):
        """Valid post deve redirecionar para /inscricao/1/"""

        # testa status 302 que é redirecionar
        # self.assertEqual(302, self.resp.status_code) # --> mudou agora redireciona e usa o teste abaixo

        # testa se foi redirecionado para /inscricao/1/
        self.assertRedirects(self.resp, '/inscricao/1/')

    def test_sent_subscribe_email(self):
        # esse mail, não manda realmente, apena guarda no outbox
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        # mandou um form vazio, dicionario vazio, para forçar os testes de erro
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST não deve ser redirecionado"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Deve usar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, "subscriptions/subscription_form.html")

    def test_has_form(self):
        """Context deve ter form SubscriptionForm"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_traz_erros(self):
        """ """
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


# @unittest.skip('A ser removido') -->
# class SubscribeSuccessMessage(TestCase):
#     def setUp(self):
#         dados = dict(name = "João Balalão",
#                      cpf = '888777666-55',
#                      email = 'lincoln@cmc.pr.gov.br',
#                      phone = '(41)3350-5813')
#         self.resp = self.client.post('/inscricao/', dados, follow = True)
#
#     def test_message(self):
#         self.assertContains(self.resp, 'Inscrição realizada com sucesso!')
