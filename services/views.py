from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Category, Tag, Order, OrderItem
from .forms import ProductForm, CategoryForm, TagForm, OrderForm, OrderItemFormSet

def product_list(request):
    """Список товаров с фильтрацией и пагинацией"""
    products = Product.objects.filter(is_deleted=False).select_related('category').prefetch_related('tags')
    
    # Фильтрация
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')
    search_query = request.GET.get('q')
    
    if category_id:
        products = products.filter(category_id=category_id)
    if tag_id:
        products = products.filter(tags__id=tag_id)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Используем annotate вместо property
    categories = Category.objects.annotate(
        active_products_count=Count('products', filter=Q(products__is_deleted=False))
    )
    tags = Tag.objects.annotate(
        active_products_count=Count('products', filter=Q(products__is_deleted=False))
    )
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'total_products': products.count(),
    }
    return render(request, 'services/product_list.html', context)

def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('tags'), 
        pk=pk, 
        is_deleted=False
    )
    
    # Похожие товары (из той же категории)
    related_products = Product.objects.filter(
        category=product.category,
        is_deleted=False
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'services/product_detail.html', context)

def category_list(request):
    """Список категорий"""
    # Используем annotate
    categories = Category.objects.annotate(
        active_products_count=Count('products', filter=Q(products__is_deleted=False))
    )
    return render(request, 'services/category_list.html', {'categories': categories})

def category_detail(request, pk):
    """Детальная страница категории с товарами"""
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, is_deleted=False)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'services/category_detail.html', context)

def tag_list(request):
    """Список тегов"""
    # Используем annotate 
    tags = Tag.objects.annotate(
        active_products_count=Count('products', filter=Q(products__is_deleted=False))
    )
    return render(request, 'services/tag_list.html', {'tags': tags})

def tag_detail(request, pk):
    """Детальная страница тега с товарами"""
    tag = get_object_or_404(Tag, pk=pk)
    products = Product.objects.filter(tags=tag, is_deleted=False)
    
    context = {
        'tag': tag,
        'products': products,
    }
    return render(request, 'services/tag_detail.html', context)

def product_create(request):
    """Создание товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Товар "{product.name}" успешно создан!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'services/forms/product_form.html', {'form': form})

def category_create(request):
    """Создание категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'services/forms/category_form.html', {'form': form})

def tag_create(request):
    """Создание тега"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'Тег "{tag.name}" успешно создан!')
            return redirect('tag_list')
    else:
        form = TagForm()
    
    return render(request, 'services/forms/tag_form.html', {'form': form})

def order_create(request):
    """Создание заказа с позициями"""
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            formset.instance = order
            formset.save()
            
            # Обновляем общую сумму
            order.calculate_total()
            
            messages.success(request, f'Заказ {order.order_number} успешно создан!')
            return redirect('product_list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    
    context = {
        'order_form': order_form,
        'formset': formset,
    }
    return render(request, 'services/forms/order_form.html', context)

def order_list(request):
    """Список заказов"""
    orders = Order.objects.prefetch_related('items').all()
    return render(request, 'services/order_list.html', {'orders': orders})

def order_detail(request, pk):
    """Детальная страница заказа"""
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=pk)
    return render(request, 'services/order_detail.html', {'order': order})

# Простые страницы
def user_profile(request):
    return render(request, 'services/profile.html')

def cart_page(request):
    return render(request, 'services/cart.html')

def settings_page(request):
    return render(request, 'services/settings.html')

def about_page(request):
    return render(request, 'services/about.html')