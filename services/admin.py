from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Tag, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'discount_amount']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'phone', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'phone']
    readonly_fields = ['order_number', 'total_amount', 'created_at']
    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'tags', 'created_at', 'is_deleted']
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']
    
    def is_available(self, obj):
        return not obj.is_deleted
    is_available.boolean = True
    is_available.short_description = 'Доступен'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_products_count', 'created_at']
    search_fields = ['name']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_deleted=False).count()
    get_products_count.short_description = 'Кол-во товаров'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'get_products_count', 'created_at']
    search_fields = ['name']
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">■</span> {}',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Цвет'
    
    def get_products_count(self, obj):
        return obj.products.filter(is_deleted=False).count()
    get_products_count.short_description = 'Кол-во товаров'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'discount', 'total_price']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'product__name']