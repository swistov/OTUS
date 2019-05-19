from views import index, my_view, post_enabled
import re


def get_view(request):
    if request['REQUEST_URI'] == '/':
        return index()
    elif request['REQUEST_URI'] == '/my_view':
        return my_view()


def post_view(requests):
    """
    :param requests: POST request from user
    :return: if OK - return user parameters, if request not have parameters -
                return None str
    """
    query_string = requests['QUERY_STRING']
    if query_string:
        return post_enabled('\n'.join(query_string.split('&')))
    else:
        return b'None'
