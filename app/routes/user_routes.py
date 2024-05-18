from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.models.blacklist import TokenBlacklist
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timezone

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/cadastro', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = bool(data.get('is_admin')) or False

    if not username:
        return jsonify({"msg": "Usuário não pode estar vazio"}), 400
    if not email:
        return jsonify({"msg": "Email não pode estar vazio"}), 400
    if not password:
        return jsonify({"msg": "Senha não pode estar vazio"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Usuário já está em uso"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email já está em uso"}), 400
    

    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuário registrado com sucesso"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Credenciais inválidas"}), 401

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now()
    db.session.add(TokenBlacklist(jti=jti, created_at=now))
    db.session.commit()

    return jsonify({"msg": "Desconectado"}), 200


@user_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    user.delete()
    return jsonify({"msg": "Usuário deletado"}), 200
