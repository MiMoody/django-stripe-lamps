def process_exception(errors=(Exception, ), default_value=''):
    """ Декоратор позволяет отлавливать и обрабатывать различные ошибки """
    
    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                print("ERROR: ", repr(e))
                return default_value

        return wrapper

    return decorator