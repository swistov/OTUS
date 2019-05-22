It's WSGI web-framework

For work module need install uWSGI module

`pip install uwsgi`

You can start for test with command

`uwsgi --http :8000 --wsgi-file wsgi.py  --enable-threads --thunder-lock`

If send GET request you can see some text in your browser.
Examples:
    
    curl -X GET http://localhost:8000/my_view
    
answer
    
    My view


If send POST request with some parameter you see parameter list and NONE is you don't send parameters.
Examples: 


    curl -X POST http://localhost:8000/?d=d

and you will get answer 

    Your parameters:
    d=d
#    
Request:

    curl -X POST http://localhost:8000
    
Answer:

    None