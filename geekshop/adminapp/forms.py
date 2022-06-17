from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from authapp.models import User
from mainapp.models import Product, ProductCategories
from authapp.validator import validate_name, validate_email


class AdminRegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput(),
                            validators=[validate_email])

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(AdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавьте фотографию'
        self.fields['age'].widget.attrs['placeholder'] = 'Возраст'

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class AdminProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'image', 'age')

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'price')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'descriptions', 'image', 'price')

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название продукта'
        self.fields['category'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите стоимость'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Введите описание продукта'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавьте фотографию'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'quantity', 'descriptions', 'image', 'price')

    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название продукта'
        self.fields['category'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите стоимость'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Введите описание продукта'
        self.fields['image'].widget.attrs['placeholder'] = 'Добавьте фотографию'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class CategoryUpdateForm(forms.ModelForm):
    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=90,
                                  initial=0)

    class Meta:
        model = ProductCategories
        fields = ('name', 'descriptions', 'discount')

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Введите описание категории'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategories
        fields = ('name', 'descriptions',)

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Введите описание категории'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control py-4'
