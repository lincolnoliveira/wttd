"""
fizzbuzz:
- quando múltiplo de 3, responde fizz
- quando múltiplo de 5, responde buzz
- quando múltiplo de 3 e 5, responde fizzbuzz
- senão, responde o número de entrada
"""

from functools import partial

# def eh_multiplo_de(testado, base):
#     return (testado % base) == 0

eh_multiplo_de = lambda testado, base: testado % base == 0

# inútil, só pra aprender o conceito mesmo
eh_multiplo_de_5 = partial(eh_multiplo_de,base=5)

def robot(i):
    retorno = str(i);
    if eh_multiplo_de(i, 15):
        retorno = 'fizzbuzz'
    elif eh_multiplo_de(i, 3):
        retorno = 'fizz'
    elif eh_multiplo_de_5(i):
        retorno = 'buzz'
    return retorno

import unittest

# define uma classe própria de testes, que herda de unittest.TestCase
class FizzBuzzTest(unittest.TestCase):
    # define os testes a serem executados (cenário de testes)
    def test_say_1_when_1(self):
        self.assertEqual(robot(1), '1')

    def test_say_2_when_2(self):
        self.assertEqual(robot(2), '2')

    def test_say_fizz_when_4(self):
        self.assertEqual(robot(4),'4')

    def test_say_fizz_when_3(self):
        self.assertEqual(robot(3),'fizz')

    def test_say_fizz_when_6(self):
        self.assertEqual(robot(6),'fizz')

    def test_say_fizz_when_12(self):
        self.assertEqual(robot(12),'fizz')

    def test_say_buzz_when_5(self):
        self.assertEqual(robot(5),'buzz')

    def test_say_buzz_when_10(self):
        self.assertEqual(robot(10),'buzz')

    def test_say__when_20(self):
        self.assertEqual(robot(20),'buzz')

    def test_say_fizzbuzz_when_15(self):
        self.assertEqual(robot(15),'fizzbuzz')

    def test_say_fizzbuzz_when_30(self):
        self.assertEqual(robot(30),'fizzbuzz')

if __name__ == '__main__':
     unittest.main()

"""
Teste inicial, sem o fw unittest

def self.assertEqual(testado, esperado):
    from sys import _getframe
    caller = _getframe().f_back
    linha = caller.f_lineno

    msg= 'Falha na linha {}: esperado {}, obtido {}'
    if not testado == esperado:
        print (msg.format(linha, esperado, testado))


if __name__ == '__main__':
    self.assertEqual(robot(1),'1')
    self.assertEqual(robot(2),'2')
    self.assertEqual(robot(4),'4')

    self.assertEqual(robot(3),'fizz')
    self.assertEqual(robot(6),'fizz')
    self.assertEqual(robot(12),'fizz')

    self.assertEqual(robot(5),'buzz')
    self.assertEqual(robot(10),'buzz')
    self.assertEqual(robot(20),'buzz')

    self.assertEqual(robot(15),'fizzbuzz')
    self.assertEqual(robot(30),'fizzbuzz')

"""