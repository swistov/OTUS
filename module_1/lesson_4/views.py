def index():
    return b'Hi my dier friend'


def my_view():
    return b'My view'


def post_enabled(query):
    return str.encode(f'Your parameters \n{query}')
