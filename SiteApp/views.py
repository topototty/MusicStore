from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import responses, Response
from rest_framework.permissions import IsAuthenticated

from .serializers import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib import messages
from .permissions import *

from .models import *

from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# --*ДЛЯ НАВИГАЦИИ*--
def HomeNavigation(request):
    return render(request, "SiteApp/index.html")
def ApiNavigation(request):
    return render(request, "SiteApp/API/api.html")
def AccountNavigation(request):
    return render(request, "SiteApp/Profile/profile.html")

#--*ДЛЯ КАТАЛОГА*--

def products_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    products = Product.objects.filter(tags=tag)
    context = {'tag': tag, 'products': products}
    return render(request, 'SiteApp/Catalog/products_by_tag.html', context)

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'SiteApp/Catalog/products_by_category.html', context)

def CallBack(request):
    back_to_catalog = reverse('catalog')
    return render(request, 'SiteApp/Catalog/callback.html')

# def category_list(request):
#     categories = Category.objects.all()
#     context = {
#              'title':'Категории',
#              'list_categories' : categories,
#          }
#     return render(request, 'SiteApp/Catalog/categories.html', context)

def tag_list(request):
    tags = Tag.objects.all()
    context = {
             'title':'Категории',
             'list_tags' : tags,
         }
    return render(request, 'SiteApp/Catalog/tags.html', context)


#--*КОНТРОЛЛЕР ДЛЯ ТОВАРОВ*--#

# Вывод товаров
class ProductList(ListView):
    model = Product
    template_name = 'SiteApp/Catalog/catalog.html'
    context_object_name = 'list_products'
    extra_context = {'title': 'Каталог'}

    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(exist=True)

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

# Вывод деталей товара
class ProductDetail(DetailView):
    model = Product

# Создание товаров

class ProductCreate(UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'SiteApp/create_product.html'
    success_url = reverse_lazy('catalog')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# Изменение товаров
class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog')

    def test_func(self):
        return self.request.user.is_superuser

# Удаление товаров
class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog')
    context_object_name = 'product'

    def test_func(self):
        return self.request.user.is_superuser

def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return redirect('catalog')
    else:
        category_form = CategoryForm()

    context = {
        'form':category_form,
    }
    return render(request, "SiteApp/create_category.html", context)

#--*КОНТРОЛЛЕР ДЛЯ КАТЕГОРИЙ*--#

# Вывод категорий
class CategoryList(ListView):
    model = Category
    template_name = 'SiteApp/Catalog/categories.html'
    context_object_name = 'list_categories'

    extra_context = {'title':'Категории'}

    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

# Вывод деталей категории
class CategoryDetail(DetailView):
    model = Category
    template_name = 'SiteApp/category_detail.html'  # Замените на ваш шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()  # Получаем объект категории
        products = Product.objects.filter(category=category)  # Фильтруем товары по категории
        context['products'] = products  # Передаем список товаров в контекст шаблона
        return context

#--*КОНТРОЛЛЕР ДЛЯ ТЭГОВ*--#

# Вывод тэгов
class TagList(ListView):
    model = Tag
    template_name = 'SiteApp/Catalog/tags.html'
    context_object_name = 'list_tags'

    extra_context = {'title':'Тэги'}

    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

# Вывод деталей тэга
class TagDetail(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        products = Product.objects.filter(tags=tag)
        context['products'] = products
        return context

# Создание тэга
class TagCreate(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'SiteApp/create_tag.html'
    success_url = reverse_lazy('tags')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


#--*КОНТРОЛЛЕР ДЛЯ ЗАКАЗОВ*--#

# Вывод заказов
class OrderList(ListView):
    model = Order
    template_name = 'SiteApp/Profile/orders.html'
    context_object_name = 'list_orders'

    paginate_by = 6
    extra_context = {'title':'Заказы'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

# Вывод деталей заказа
class OrderDetail(DetailView):
    model = Order
    template_name = 'SiteApp/Profile/order_detail.html'

# Создание заказа
class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'SiteApp/Profile/create_order.html'
    success_url = reverse_lazy('orders')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# Изменение заказа
class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'SiteApp/Profile/order_form.html'
    success_url = reverse_lazy('orders')

    def test_func(self):
        return self.request.user.is_superuser


# Удаление заказа

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')

    def test_func(self):
        return self.request.user.is_superuser


#--*ДЛЯ ПРОФИЛЯ*--
def Settings(request):
    return render(request, "SiteApp/Profile/settings.html")

def Orders(request):
    return render(request, "SiteApp/Profile/orders.html")

def Favourites(request):
    return render(request, "SiteApp/Profile/favourites.html")

#--*КОРЗИНА*--

@login_required(login_url=reverse_lazy('home')) # Проверка авторизации пользователя, если не авторизован - будет направлен на страницу home
def Cart(request):
    return render(request, 'SiteApp/cart.html')

# --*АПИШКА*--
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (CRUDPermissions, IsAuthenticated)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (CRUDPermissions, IsAuthenticated)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (CRUDPermissions, IsAuthenticated)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (CRUDPermissions, IsAuthenticated)

def AddData(request):
    return render(request, "SiteApp/API/add_data.html")

def UpdateData(request, id):
    return render(request, "SiteApp/API/update_data.html", {'id': id})

def DeleteData(request, id):
    return render(request, "SiteApp/API/delete_data.html", {'id': id})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
            return render(request, 'SiteApp/login.html')
    return render(request, 'SiteApp/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле "{form.fields[field].label}": {error}')
            return redirect('signup')
    else:
        form = UserCreationForm()
    return render(request, 'SiteApp/signup.html', {'form': form})
def log_out(request):
    logout(request)
    return redirect(reverse_lazy('home'))