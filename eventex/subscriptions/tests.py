from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


# cada classe dessa é um cenário de testes
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

class SubscribePostTest(TestCase):
    def setUp(self):
        dados = dict(name = "João Balalão",
                     cpf = '888777666-55',
                     email = 'lincoln@cmc.pr.gov.br',
                     phone = '(41)3350-5813')
        self.resp = self.client.post('/inscricao/', dados)

    def test_post(self):
        """Valid post deve redirecionar para /inscricao/"""
        # testa status 302 que é redirecionar
        self.assertEqual(302, self.resp.status_code)

    def test_sent_subscribe_email(self):
        # esse mail, não manda realmente, apena guarda no outbox
        self.assertEqual(1, len(mail.outbox))

    def test_assunto_do_email(self):
        email = mail.outbox[0]
        self.assertEqual('Confirmação de inscrição',email.subject)

    def test_remetente_do_email(self):
        email = mail.outbox[0]
        self.assertEqual('contato@eventex.com.br',email.from_email)

    def test_destinatario_do_email(self):
        email = mail.outbox[0]
        self.assertEqual(['contato@eventex.com.br','lincoln@cmc.pr.gov.br' ],email.to)

    def test_corpo_do_email(self):
        email = mail.outbox[0]
        self.assertIn('João Balalão',email.body)
        self.assertIn('888777666-55',email.body)
        self.assertIn('lincoln@cmc.pr.gov.br',email.body)
        self.assertIn('(41)3350-5813',email.body)

class SubscribeInvalidPostTest(TestCase):
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

class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        dados = dict(name = "João Balalão",
                     cpf = '888777666-55',
                     email = 'lincoln@cmc.pr.gov.br',
                     phone = '(41)3350-5813')
        self.resp = self.client.post('/inscricao/', dados, follow = True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')
