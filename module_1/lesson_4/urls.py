from views import index, my_view, post_enabled


class Routes:
    """
    Dict with all routes
    """
    site_routes = {
        '/': index(),
        '/my_view': my_view(),
    }


def get_view(request):
    """
    :param request: User request
    :return: Func from Routers if not in dict - return '/'
    """
    routes = Routes.site_routes.get(request['REQUEST_URI'])

    if routes is None:
        return Routes.site_routes.get('/')

    return routes


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
        return b'NONE'
