from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    # cria o context, um dict, mapeando form.
    # esse SubscriptionForm vai ter que estar definido em forms.py
    context = {'form': SubscriptionForm()}
    # renderiza a resposta, conecta o html com o form (context)
    return render(request, 'subscriptions/subscription_form.html', context)