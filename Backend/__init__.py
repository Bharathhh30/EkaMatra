from flask import Flask
from flask_login import LoginManager



# Creating flask app 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "First Secret key"
    app.secret_key='my_secret_key'
    # Registering the blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Registering the blueprint
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')


    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return get_user_by_id(user_id)
        except:
            return None
        
    @app.template_filter('next')
    def next_filter(iterable):
        return next(iterable, None)



    return app