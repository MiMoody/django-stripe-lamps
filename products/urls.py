from django.urls import path
from . import views

urlpatterns = [
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('', views.ProductPageView.as_view(), name='product'),
    path('products', views.ListProductView.as_view(), name='products'),
    path('item/<pk>/<slug:currency_code>', views.DetailProductView.as_view(), name='detail-product'),
    path('buy/<pk>/<slug:currency_code>', views.CheckoutSessionOneProduct.as_view(), name='session-one'),
    path('order/<slug:currency_code>', views.CheckoutSessionMoreProduct.as_view(), name='session-more'),
    path('cart', views.CardProductView.as_view(), name='cart'),
    path('list-cart-product/<slug:currency_code>', views.ListCartProductView.as_view(), name='list-cart'),
    
]
