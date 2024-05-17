from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes.user_routes import user_bp
from app.models.blacklist import TokenBlacklist
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlacklist.query.filter_by(jti=jti).first()
    
    return token is not None

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = '346f1cc60c2c434f93ce02946f5a562f'

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api/users')

    with app.app_context():
        db.create_all()

    return app
