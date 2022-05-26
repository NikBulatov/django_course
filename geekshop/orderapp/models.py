from django.conf import settings
from django.db import models

# Create your models here.
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCESSED = 'STP'
    PAID = 'PD'
    PROCESSED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNL'

    ORDER_STATUS_CHOICES = ((FORMING, 'Формируется'),
                            (SEND_TO_PROCESSED, 'Отправлен в обработку'),
                            (PAID, 'Оплачен'),
                            (PROCESSED, 'В процессе'),
                            (READY, 'Готов к выдаче'),
                            (CANCEL, 'Отменён'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создан', auto_now=True)
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=True)
    paid = models.DateTimeField(verbose_name='Оплачен', null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='Статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self) -> str:
        return f'Текущий заказ {self.pk}'

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item_ in self.orderitems.select_related():
            item_.product.quantity += item_.quantity
            item_.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товары', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk).quantity
