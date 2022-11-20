from django.contrib import admin
from .models import (
    Product,
    ProductPrice,
    ContentProductOrder,
    CurrencyType,
    ProductOrder,
    OrderStatus,
    ProductCart
    )


admin.site.register(Product)
admin.site.register(CurrencyType)
admin.site.register(ProductPrice)
admin.site.register(ContentProductOrder)
admin.site.register(ProductOrder)
admin.site.register(OrderStatus)
admin.site.register(ProductCart)