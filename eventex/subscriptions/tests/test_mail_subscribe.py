from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        dados = dict(name = "João Balalão",
                     cpf = '888777666-55',
                     email = 'lincoln@cmc.pr.gov.br',
                     phone = '(41)3350-5813')
        self.resp = self.client.post('/inscricao/', dados)
        self.email = mail.outbox[0]

    def test_assunto_do_email(self):
        self.assertEqual('Confirmação de inscrição',self.email.subject)

    def test_remetente_do_email(self):
        self.assertEqual('contato@eventex.com.br',self.email.from_email)

    def test_destinatario_do_email(self):
        self.assertEqual(['contato@eventex.com.br','lincoln@cmc.pr.gov.br' ],self.email.to)

    def test_corpo_do_email(self):
        contents= ['João Balalão','888777666-55',
                   'lincoln@cmc.pr.gov.br',
                   '(41)3350-5813']
        for cont in contents:
            with self.subTest():
                self.assertIn(cont,self.email.body)
