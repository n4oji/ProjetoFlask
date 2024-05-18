from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '346f1cc60c2c434f93ce02946f5a562f'

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.learning_path_routes import learning_path_bp
    from app.routes.course_routes import course_bp
    from app.routes.lesson_routes import lesson_bp
    from app.routes.comment_routes import comment_bp
    from app.routes.rating_routes import rating_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(learning_path_bp, url_prefix='/api')
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(lesson_bp, url_prefix='/api')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(rating_bp, url_prefix='/api')


    with app.app_context():
        db.create_all()

    return app
