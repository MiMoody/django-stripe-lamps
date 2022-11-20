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
    

class OrderStatus(models.Model):
    """ Класс хранит статусы заказов """
    
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.status
    
    
class ProductOrder(models.Model):
    """ Привязка продуктов к определенному заказу """
    
    form_time = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(OrderStatus, related_name="order_status", on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return f"{self.form_time} {self.status.status}"


class ContentProductOrder(models.Model):
    """ Связующая таблица для хранения информации 
        о принадлежности продуктов к заказу и вспомогательной информации
    """
    
    product_order = models.ForeignKey(ProductOrder, 
                                      related_name="order_product", 
                                      on_delete=models.PROTECT)
    product_price = models.ForeignKey(ProductPrice, 
                                      related_name="order_product_price", 
                                      on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.product_order.id} {self.product_price.product.name}"
    

class ProductCart(models.Model):
    """ Класс хранит информацию о добавленных в корзину продуктов (без привязки к пользователю) """

    product_price = models.ForeignKey(ProductPrice, related_name="price_cart", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product_price.product.name}"

    
    
    