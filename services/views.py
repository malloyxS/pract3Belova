from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category, Tag, Order
from .forms import ProductForm, CategoryForm, TagForm, OrderForm

def home_page(request):
    """Главная страница"""
    return redirect('product_list')

def product_list(request):
    """Страница каталога товаров"""
    products = Product.objects.filter(is_deleted=False)
    
    # Фильтрация по категориям и тегам
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    
    if category_id:
        products = products.filter(category_id=category_id)
    if tag_id:
        products = products.filter(tags__id=tag_id)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'services/product_list.html', {
        'products': products,
        'categories': categories,
        'tags': tags,
    })

def product_detail(request, product_id):
    """Страница просмотра товара по ID"""
    product = get_object_or_404(Product, pk=product_id, is_deleted=False)
    return render(request, 'services/product_detail.html', {'product': product})

def category_list(request):
    """Страница категорий"""
    categories = Category.objects.all()
    return render(request, 'services/category_list.html', {'categories': categories})

def tag_list(request):
    """Страница тегов"""
    tags = Tag.objects.all()
    return render(request, 'services/tag_list.html', {'tags': tags})

def product_create(request):
    """Создание товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'services/forms/product_form.html', {'form': form})

def category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'services/forms/category_form.html', {'form': form})

def tag_create(request):
    """Создание тега"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'services/forms/tag_form.html', {'form': form})

def order_create(request):
    """Создание заказа"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number = f"ORD-{Order.objects.count() + 1:06d}"
            order.save()
            return redirect('product_list')
    else:
        form = OrderForm()
    return render(request, 'services/forms/order_form.html', {'form': form})

def user_profile(request):
    """Страница личного кабинета"""
    return render(request, 'services/profile.html')

def cart_page(request):
    """Страница корзины"""
    return render(request, 'services/cart.html')

def settings_page(request):
    """Страница настроек"""
    return render(request, 'services/settings.html')

def about_page(request):
    """Страница о нас"""
    return render(request, 'services/about.html')