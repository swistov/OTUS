from urls import get_view, post_view


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    if environ['REQUEST_METHOD'] == 'GET':
        return get_view(environ)
    elif environ['REQUEST_METHOD'] == 'POST':
        return post_view(environ)
    else:
        start_response('404 OK', [('Content-Type', 'text/plain')])
        return b'Your method must be GET or POST'
