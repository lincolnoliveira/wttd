from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    # full_clean sanitiza os campos de um form e converte para os tipos adequados
    # vai criar o cleaned_data com tudo certo
    # form.full_clean()  # não precisa chamar porque o is_valid o chama internamente

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _envia_email('Confirmação de inscrição',
                 settings.DEFAULT_FROM_EMAIL,
                 subscription.email,
                 'subscriptions/subscription_email.txt',
                 # form.cleaned_data)
                 {'subscription': subscription})

    # não vai mais mandar msg, vai redirecionar
    # messages.success(request, 'Inscrição realizada com sucesso!')

#    return HttpResponseRedirect('/inscricao/1/')
    return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))


def _envia_email(subject, from_email, to_email, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_email, [from_email, to_email])


def new(request):
    # cria o context, um dict, mapeando form.
    # esse SubscriptionForm vai ter que estar definido em forms.py
    context = {'form': SubscriptionForm()}
    # renderiza a resposta, conecta o html com o form (context)
    return render(request, 'subscriptions/subscription_form.html', context)


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk = pk)
    except Subscription.DoesNotExist:
        raise Http404



    return render(request, 'subscriptions/subscription_detail.html',
                  {'subscription': subscription})

