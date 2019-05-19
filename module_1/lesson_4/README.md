It's WSGI web-framework

For work module need install uWSGI module

`pip install uwsgi`

You can start for test with next command

`uwsgi --http :8000 --wsgi-file wsgi.py  --enable-threads --thunder-lock`

If send GET request you can see some text in your browser.
If send POST request with some parameter you see parameter list and NONE is you don't send parameters. 