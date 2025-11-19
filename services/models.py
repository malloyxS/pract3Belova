from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
import uuid

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])
    
    @property
    def products_count(self):
        return self.products.filter(is_deleted=False).count()

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название тега")
    color = models.CharField(max_length=7, default='#007bff', verbose_name="Цвет")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tag_detail', args=[str(self.id)])
    
    @property
    def products_count(self):
        return self.products.filter(is_deleted=False).count()

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена",
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        verbose_name="Категория"
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        related_name='products', 
        verbose_name="Теги"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_deleted = models.BooleanField(default=False, verbose_name="Логическое удаление")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.price}₽"
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    def is_available(self):
        return not self.is_deleted

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', '🆕 Новый'),
        ('processing', '🔄 В обработке'),
        ('shipped', '🚚 Отправлен'),
        ('delivered', '✅ Доставлен'),
        ('cancelled', '❌ Отменен'),
    ]
    
    order_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Номер заказа",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    customer_name = models.CharField(max_length=200, verbose_name="ФИО клиента")
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='new', 
        verbose_name="Статус"
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name="Общая сумма"
    )
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Заказ {self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])
    
    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Скидка (%)",
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена за единицу",
        default=0  # Добавляем значение по умолчанию
    )
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        if not self.price or self.price == 0:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.calculate_total()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.calculate_total()
    
    @property
    def total_price(self):
        discounted_price = self.price * (1 - self.discount / 100)
        return discounted_price * self.quantity
    
    @property
    def discount_amount(self):
        return self.price * (self.discount / 100) * self.quantity