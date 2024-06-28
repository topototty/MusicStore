import uuid

from django.db import models
from django.urls import reverse, reverse_lazy

# Товар
class Product(models.Model):
    name = models.CharField(default='Продукт', verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=11, decimal_places=2, default=100.00, verbose_name="Цена")
    date_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    data_update = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    exist = models.BooleanField(default=True, verbose_name="Существует?")

    photo = models.ImageField(null=True, blank=True, upload_to='image/%Y/%m/%d', verbose_name="Фото")

    category = models.ForeignKey('category', on_delete=models.PROTECT, null=True, related_name='categories', verbose_name='Категория' ) # Кавычки для того, чтобы обратиться к классу, который находится ниже. Связь 1 ко многим
    tags = models.ManyToManyField('tag', related_name='tags', verbose_name='Тэг')

    def __str__(self):
        return f'{self.name} - {self.price}'

    def get_absolute_url(self):
        return reverse_lazy('product_detail')

    class Meta:
        verbose_name="Продукт" # Имя самой модели
        verbose_name_plural="Продукты" # Это чтобы множественное число было адекватным
        ordering=['name', '-price'] # Сортировка по атрибутам. "-" - это типа "!"


#Категория
class Category(models.Model):
    name = models.CharField(default='Категория', verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name="Категория"
        verbose_name_plural="Категории"
        ordering=['name', ]


#Тэг
class Tag(models.Model):
    name = models.CharField(default='Тэг', verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name="Тэг"
        verbose_name_plural="Тэги"
        ordering=['name', ]

    def __str__(self):
        return f'{self.name}'


# Заказ
class Order(models.Model):
    order_number = models.AutoField(primary_key=True, editable=False, verbose_name='Номер заказа')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.CharField(max_length=100, verbose_name='Адрес')
    client_phone = models.CharField(max_length=11, verbose_name='Телефон')
    client_name = models.CharField(max_length=50, verbose_name='ФИО')

    def __str__(self):
        return str(self.order_number)

    class Meta:
        verbose_name="Заказ"
        verbose_name_plural = "Заказы"
        ordering=['order_number',]


# Промежуточная таблица "позиция заказа"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Заказ')
    product = models.ForeignKey('product', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка')

    def __str__(self):
        return f'{self.order} - {self.product}'

    class Meta:
        verbose_name="Позиция заказа"
        verbose_name_plural = "Позиции заказов"
