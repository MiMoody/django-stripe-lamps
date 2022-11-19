from django.conf import settings


class NotFoundCurrencyCoef(Exception):
    """ Исключение при отсутствии коэффицента для конверта валюты """
    
    
def convert_price_currency_by_stipe(currency_code :str, price :int):
    """ Конвертирует валюту к формату stripe,
        так как рубли должны быть в копейках,
        а доллары в центах
    """
    currency_coef :int = settings.STRIPE_CURRENCY.get(currency_code) 
    
    if not currency_coef:
        raise NotFoundCurrencyCoef
    
    return currency_coef * price