It's a demo internet magazine on the Django

For start project needs intsall Flask pakage and play the command

    pip install -r requirements.txt
    
Move to work directory, migrate DB, create super-user and start project

    cd otus/
    pythom manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

For open suite need open
    
    http://127.0.0.1:8000
