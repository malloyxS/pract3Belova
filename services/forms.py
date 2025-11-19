from django import forms
from .models import Product, Category, Tag, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'price': 'Цена (₽)',
            'image': 'Изображение',
            'category': 'Категория',
            'tags': 'Теги'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название категории'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите описание категории'
            }),
        }
        labels = {
            'name': 'Название категории',
            'description': 'Описание'
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название тега'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
        }
        labels = {
            'name': 'Название тега',
            'color': 'Цвет'
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'delivery_address']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов Иван Иванович'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите полный адрес доставки'
            }),
        }
        labels = {
            'customer_name': 'ФИО клиента',
            'phone': 'Телефон',
            'delivery_address': 'Адрес доставки'
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'discount']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '1'
            }),
        }
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
            'discount': 'Скидка (%)'
        }

OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)