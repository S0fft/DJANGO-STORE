from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name: str = 'orders/success.html'
    title: str = 'Thank you for your order!'


class CanceledTemplateView(TemplateView):
    template_name: str = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    title: str = 'SyCloth - Placing an order'
    template_name: str = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OHNJFIK1qsOXGQxSLfqjTb9',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user

        return super().form_valid(form)
