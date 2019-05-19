from views import index, my_view, post_enabled
import re


def get_view(request):
    if request['REQUEST_URI'] == '/':
        return index()
    elif request['REQUEST_URI'] == '/my_view':
        return my_view()


def post_view(requests):
    if requests['QUERY_STRING']:
        return post_enabled(requests['QUERY_STRING'])
    else:
        return b'DEAD'
