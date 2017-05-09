from django.test import TestCase

class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get("/")

    def test_get_code(self):
        """ GET / should return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Should use index.html"""
        self.assertTemplateUsed(self.resp, "index.html")

    def test_link_inscricao(self):
        """Verifica existência de link para página de inscricao"""
        self.assertContains(self.resp, 'href="/inscricao/"')
