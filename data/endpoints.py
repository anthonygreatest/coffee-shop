
from urllib.parse import urlencode



class Endpoints:

    BASE_URL = 'https://valentinos-coffee.herokuapp.com'
    PRODUCTS = '/products'
    CLIENTS = '/clients'
    ORDERS = '/orders'
    STATUS = '/status'



def url_maker(path, data=None):
    if not data:
        return f'{Endpoints.BASE_URL}{path}'
    else:
        url = f'{Endpoints.BASE_URL}{path}'
        params = {key: value for key, value in data.__dict__.items() if value is not None}
        return f'{url}?{urlencode(params, doseq=True)}' if params else url
