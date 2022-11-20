from typing import List
from django.db.models import QuerySet
from .utils import convert_price_currency_by_stipe
from products.models import ProductCart


def create_stripe_payment_items(products :QuerySet[ProductCart], currency_code :str) ->List[dict]:
    """ Создание объекта stripe line_items с несколькими товарами """
    
    line_items :List[dict] = []
    
    for product in products:
        line_items.append({
            "price_data":{
                "currency":currency_code,
                "unit_amount":convert_price_currency_by_stipe(currency_code, 
                                                              int(product.product_price.price)),
                "product_data":{
                    "name":product.product_price.product.name,
                    # "images": [product.product_price.product.image,]
                }
            },
            "quantity":product.quantity
        })
    return line_items