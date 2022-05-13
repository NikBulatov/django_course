from django import forms
from authapp.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from orderapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    # price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs['class'] = 'form-control'


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderItemsForm, self).__init__(*args, **kwargs)
        for filed in self.fields.values():
            filed.widget.attrs['class'] = 'form-control'
