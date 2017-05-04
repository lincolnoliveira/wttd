from django import forms


class SubscriptionForm(forms.Form):
    # criamos os 4 campos dinâmicos do form
    name = forms.CharField(label='Nome:')
    cpf = forms.CharField(label='CPF:')
    email = forms.EmailField(label='e-mail')
    phone = forms.CharField(label='Fone:')
