import json
from django.shortcuts import render
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import F 
from .business_logic.utils import convert_price_currency_by_stipe
from .business_logic.try_except import process_exception
from .models import Product, CurrencyType, ProductPrice, ProductCart


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "products/success.html"


class CancelView(TemplateView):
    template_name = "products/cancel.html"


class ProductPageView(View):
    """ Главная страница товаров """
    
    @process_exception(default_value=HttpResponse("""<h1>Error loading products! Please contact your system administrator </h1>""",status=400))
    def get(self, request):
        
        currencies = CurrencyType.objects.all()
        return render(request, 
                      "products/product.html", 
                      {
                        "currencies": currencies,
                        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
                      })
        

class DetailProductView(View):
    """ Страница с детальной информацией о товаре """
    
    @process_exception(default_value=HttpResponse("""<h1>Error loading product! Please contact your system administrator </h1>""",status=400))
    def get(self, request, pk :int, currency_code :str):
        product = Product.objects \
            .filter(price_product__currency__code = currency_code,
                    pk=pk) \
            .values(
                "id",
                "name",
                "description",
                "image",
                price = F("price_product__price"),
                currency_name = F("price_product__currency__name"),
                currency_code = F("price_product__currency__code"),
            ).first()
            
        return render(request, 
                      "products/detail_product.html", 
                      {
                       "product":product,
                       "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
                      })


class ListProductView(View):
    """ Возвращает список товаров в системе """
    
    @process_exception(default_value=JsonResponse(data={"unexpected_error":1},status=400))
    def get(self, request):
        
        currency_code = request.GET.get('currency')
        if not currency_code:
            return JsonResponse(status = 400, data = {"empty_currency_type":1})
        
        products = Product.objects.filter(price_product__currency__code = currency_code ) \
            .values(
                "id",
                "name",
                "description",
                "image",
                price = F("price_product__price"),
                currency_name = F("price_product__currency__name"),
                currency_code = F("price_product__currency__code"),
            ) 
        return render(request, 
                      "products/list_product.html", 
                      {"products": products})


class CardProductView(View):
    """ Временное хранение продуктов в корзине (без привязки к определенному пользователю)"""
    
    @process_exception(default_value=JsonResponse(data={"unexpected_error":1},status=400))
    def get(self, request):
        
        currencies = CurrencyType.objects.all()
        return render(request, 
                      'products/cart.html',
                      {
                        "currencies": currencies,
                        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
                      })
        
    
    @process_exception(default_value=JsonResponse(data={"unexpected_error":1},status=400))
    def post(self, request):
        """ Добавление товара в корзину """

        body = json.loads(request.body)
        product_id = body.get('product_id')
        currency_code = body.get('currency_code')
        quantity = body.get('quantity')
        if not product_id:
            return JsonResponse(status = 400, data = {"empty_product_id":1})
        if not currency_code:
            return JsonResponse(status = 400, data = {"empty_currency_code":1})
        if not quantity:
            quantity = 1
        try:
            price_product = ProductPrice.objects.get(product_id=product_id, currency__code=currency_code)
            product_cart = ProductCart.objects.filter(product_price=price_product).first()
            if product_cart:
                product_cart.quantity+=quantity
                product_cart.save()
            else:
                ProductCart.objects.create(product_price=price_product, quantity=quantity)
            
        except ProductPrice.DoesNotExist:
            return JsonResponse(status = 400, data = {"not_found_product_price":1})
        return JsonResponse(status = 200, data = {"success":1})
    
    @process_exception(default_value=JsonResponse(data={"unexpected_error":1},status=400))
    def delete(self, request):
        """ Удаление продукта из корзины """
        
        body = json.loads(request.body)
        product_id = body.get('product_id')
        currency_code = body.get('currency_code')
        if not product_id:
            return JsonResponse(status = 400, data = {"empty_product_id":1})
        if not currency_code:
            return JsonResponse(status = 400, data = {"empty_currency_code":1})
        ProductCart.objects.filter(product_price__product__id=product_id,
                                   product_price__currency__code=currency_code).delete()
        return JsonResponse(status = 200, data = {"success":1})


class ListCartProductView(View):
    """ Представление для подгрузки товаров из корзины """
    
    def get(self, request, currency_code :str):
        
        cart_products = ProductCart.objects.filter(product_price__currency__code=currency_code) \
                                    .values(
                                        "quantity",
                                        product_id = F("product_price__product__id"),
                                        name = F("product_price__product__name"),
                                        image = F("product_price__product__image"),
                                        price = F("product_price__price"),
                                        currency_code = F("product_price__currency__code"),
                                        currency_name = F("product_price__currency__name"))
        
        return render(request, 
                      'products/list_cart_product.html',
                      {"cart_products": cart_products})


class CheckoutSessionOneProduct(View):
    """ Создание checkout session для одного продукта """
    
    @process_exception(default_value=JsonResponse(data={"unexpected_error":1},status=400))
    def get(self, request, pk :int, currency_code :str):
        product = ProductPrice.objects.filter(currency__code = currency_code, product_id = pk ) \
            .values(
                "product_id",
                "price",
                name = F("product__name"),
                image = F("product__image"),
            ).first()
        quantity = request.GET.get("quantity", 1)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': currency_code,
                        'unit_amount': convert_price_currency_by_stipe(currency_code, int(product["price"])),
                        'product_data': {
                            'name': product["name"],
                            #'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': quantity,
                },
            ],
            metadata={
                "product_id": product['product_id']
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })