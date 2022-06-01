from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from adminapp.mixins import BaseClassContextMixin
from basket.models import Basket
from mainapp.models import Product
from orderapp.forms import OrderItemsForm
from orderapp.models import Order, OrderItem


class OrderListView(ListView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop | Order List'


class OrderCreateView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Create Order'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        order_form_set = inlineformset_factory(Order, OrderItem, OrderItemsForm, extra=1)  # extra - это поле
        if self.request.POST:
            formset = order_form_set(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                order_form_set = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_item.count())
                formset = order_form_set()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                basket_item.delete()
            else:
                formset = order_form_set()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Update Order'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data()
        order_form_set = inlineformset_factory(Order, OrderItem, OrderItemsForm)
        if self.request.POST:
            formset = order_form_set(self.request.POST, instance=self.object)
        else:
            formset = order_form_set(instance=self.object)
            for idx, form in enumerate(formset.forms):
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderUpdateView, self).form_valid(form)


class OrderReadView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop | Detail Order'


class OrderDeleteView(DeleteView, BaseClassContextMixin):
    model = Order
    success_url = reverse_lazy('orders:list')
    title = 'GeekShop | Delete Order'


def order_forming_complete(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.SEND_TO_PROCESSED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.get(pk=pk)
        if product:
            return JsonResponse({'price': product.price})
        return JsonResponse({'price': 0})

# Signals
# @receiver(pre_save, sender=OrderItem)
# @receiver(pre_save, sender=Basket)
# def product_quantity_save(sender, instance, **kwargs):
#     if instance.pk:
#         item = instance.get_item(instance.pk)
#         instance.product.quantity -= instance.quantity - item
#     else:
#         instance.product.quantity -= instance.quantity
#     instance.product.save()
#
#
# @receiver(pre_delete, sender=OrderItem)
# @receiver(pre_delete, sender=Basket)
# def product_quantity_delete(sender, instance, **kwargs):
#     instance.product.quantity += instance.quantity
#     instance.save()
