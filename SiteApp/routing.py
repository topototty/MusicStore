from django.urls import path, re_path, include
from .views import *
from SiteApp import views as v
from rest_framework import routers

order_patterns = [
    path('', v.OrderList.as_view(), name="orders"),
    path('add_order/', v.OrderCreate.as_view(), name="add_order"),
    path('order_detail/<int:pk>/', v.OrderDetail.as_view(), name="order_detail"),
    path('update_order/<int:pk>/', v.OrderUpdate.as_view(), name="order_detail_update"),
    path('order/<int:pk>/delete/', v.ProductDelete.as_view(), name='order_delete'),
]

product_categories_pattern = [
    path('', v.CategoryList.as_view(), name="categories"),
    path('category_detail/<int:pk>/', v.CategoryDetail.as_view(), name="category_detail"),
    path('tags/', v.tag_list, name="tags"),
]

account_patterns = [
    path('', v.AccountNavigation, name="profile"),
    path('settings/', v.Settings, name="settings"),

    path('orders/', include(order_patterns)),
    path('update_order/<int:pk>/', v.OrderUpdate.as_view(), name="update_order"),
    path('add_order/', v.OrderCreate.as_view(), name="add_order"),
    path('order_detail/<int:pk>/', v.OrderDetail.as_view(), name="order_detail"),
    path('order/<int:pk>/delete/', v.OrderDelete.as_view(), name='order_delete'),

    path('favourites/', v.Favourites, name='favourites')
]


catalog_patterns = [
    path('callback/', v.CallBack, name="callback"),
    path('categories/', include(product_categories_pattern)),

    path('list_products/', v.ProductList.as_view(), name="catalog"),
    path('add_product/', v.ProductCreate.as_view(), name="add_product"),
    path('product_detail/<int:pk>/', v.ProductDetail.as_view(), name="product_detail"),
    path('update/<int:pk>/', v.ProductUpdate.as_view(), name="product_detail_update"),
    path('products/<int:pk>/delete/', v.ProductDelete.as_view(), name='product_delete'),

    path('add_category/', v.add_category, name="add_category"),
    path('products_by_tag/<int:tag_id>/', v.products_by_tag, name='products_by_tag'),
    path('products_by_category/<int:category_id>/', v.products_by_category, name='products_by_category'),

    path('add_tag/', v.TagCreate.as_view(), name="add_tag"),
    path('tag_detail/<int:pk>', v.TagDetail.as_view(), name="tag_detail"),
    path('list_tags/', v.TagList.as_view(), name="tags"),

]

router_products = routers.SimpleRouter()
router_products.register(r'products', ProductViewSet)

router_tags = routers.SimpleRouter()
router_tags.register(r'tags', TagViewSet)

router_categories = routers.SimpleRouter()
router_categories.register(r'categories', CategoryViewSet)

router_orders = routers.SimpleRouter()
router_orders.register(r'orders', OrderViewSet)

api_patterns = [
    path('', v.ApiNavigation, name="api"),
    path('v1/', include(router_products.urls)),
    path('v2/', include(router_tags.urls)),
    path('v3/', include(router_categories.urls)),
    path('v4/', include(router_orders.urls)),
    # path('api_product_list/', v.GetProductListApi.as_view() , name="api_product_list"),
    # path('api_product_detail/<str:pk>/', v.GetProductDetailApi.as_view(), name="api_product_detail"),
    # path('api_add_product/', v.CreateProductApi, name="create_product"),
    path('add/', v.AddData, name="add"),
    path('update/<int:id>/', v.UpdateData, name="update"),
    path('delete/<int:id>/', v.DeleteData, name="delete"),
]

urlpatterns = [
    path('', v.HomeNavigation, name="home"),
    path('catalog/', include(catalog_patterns)),
    path('api/', include(api_patterns)),
    path('profile/', include(account_patterns)),
    path('cart/', v.Cart, name="cart"),
    path('logout/', v.log_out, name="logout"),
    path('login/', v.login_view, name="login"),
    path('signup/', v.signup_view, name="signup"),
]


