def index():
    return b'Hi my dier friend'


def my_view():
    return b'My view'


def post_enabled(query):
    """
    :param query: Query from request
    :return: byte code
    """
    return str.encode(f'Your parameters: \n{query}')
