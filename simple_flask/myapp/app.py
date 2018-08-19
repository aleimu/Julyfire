from flask import Flask
from .views.simple_page import simple_page
from .views.simple_view import simple_view
from myapp.models import db

print ("__name__",__name__)
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(simple_page, url_prefix='/pages')
app.register_blueprint(simple_view, url_prefix='/views')

db.init_app(app)

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run()
