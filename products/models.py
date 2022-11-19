from django.db import models


class Product(models.Model):
    """ Класс для описания продукта """
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_files/", blank=True, null=True)

    def __str__(self):
        return self.name
    

class CurrencyType(models.Model):
    """Класс для хранения типов валют"""
    
    code = models.CharField(max_length=20, unique=True,)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

class ProductPrice(models.Model):
    """ Связующий класс для описания дополнительных атрибутов продукта """
    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.ForeignKey(
        CurrencyType, 
        related_name="price_currency", 
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product, related_name="price_product", 
        on_delete=models.PROTECT,
        blank=True,
        null = True
    )
    
    def __str__(self):
        return f"{self.product.name} {self.currency.name} {self.price}"
    
class ContentProductOrder(models.Model):
    """ Связующая таблица для хранения информации 
        о принадлежности продуктов к заказу и вспомогательной информации
    """
    
    product_order = models.ForeignKey("ContentProductOrder", 
                                      related_name="order_product", 
                                      on_delete=models.PROTECT)
    product_price = models.ForeignKey(ProductPrice, 
                                      related_name="order_product_price", 
                                      on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.product_order} {self.product_price.product.name}"

class ProductOrder(models.Model):
    """ Привязка продуктов к определенному заказу """
    
    product_order = models.ForeignKey(
        ContentProductOrder, related_name="content_order_product", 
        on_delete=models.PROTECT,
    )
    form_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.form_time} {self.total_price}"
    
    
class ProductCart(models.Model):
    """ Класс хранит информацию о добавленных в корзину продуктов (без привязки к пользователю) """

    product_price = models.ForeignKey(ProductPrice, related_name="price_cart", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product_price.product.name}"

    
    
    