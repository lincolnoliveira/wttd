from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # full_clean sanitiza os campos de um form e converte para os tipos adequados
            # vai criar o cleaned_data com tudo certo
            #form.full_clean()  # não precisa chamar porque o is_valid o chama internamente
            mensagem = render_to_string('subscriptions/subscription_email.txt',form.cleaned_data)
            mail.send_mail('Confirmação de inscrição',
                           mensagem,
                           'contato@eventex.com.br',
                           ['contato@eventex.com.br', form.cleaned_data['email']])
            messages.success(request,'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html',{'form':form})
    else:
        # cria o context, um dict, mapeando form.
        # esse SubscriptionForm vai ter que estar definido em forms.py
        context = {'form': SubscriptionForm()}
        # renderiza a resposta, conecta o html com o form (context)
        return render(request, 'subscriptions/subscription_form.html', context)