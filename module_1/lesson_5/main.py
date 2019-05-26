from flask import Flask, request, render_template

from laptops_views import laptops_app
from app_config import laptops

app = Flask(__name__)
app.register_blueprint(laptops_app, url_prefix='/laptops/')


@app.route('/')
def index_page():
    response = render_template(
        'index.html',
        laptops=laptops,
    )
    return response


if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)


