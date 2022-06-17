from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from prettytable import PrettyTable

from mainapp.models import ProductCategories, Product
from orderapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_timedelta = timedelta(hours=12)
        action_2_timedelta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated__lte=F(
            'order__created') + action_1_timedelta)  # if order__updated <= F('order_created')+action_1_timedelta else None

        action_2_condition = (Q(order__updated__gt=F('order__created') + action_1_timedelta) &
                              (Q(order__updated__lte=F('order__created') + action_1_timedelta)))

        action_3_condition = Q(order__updated__gt=F('order__created') + action_2_timedelta)

        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        test_data = OrderItem.objects.annotate(  # добавления поля в объект QuerySet
            action_order=Case(
                action_1_order, action_2_order, action_3_order, output_field=IntegerField()
            )).annotate(
            total_price=Case(
                action_1_price, action_2_price, action_3_price, output_field=DecimalField())
        ).order_by('action_order', 'total_price').select_related()

        t_list = PrettyTable(['Order', 'Item', 'Discount', 'Time Delta'])
        for order_item in test_data:
            t_list.add_row([f'{order_item.action_order} order №{order_item.pk}',
                            f'{order_item.product.name:15}', f'{abs(order_item.total_price):6.2f} rub',
                            order_item.order.updated - order_item.order.created])
        print(t_list)