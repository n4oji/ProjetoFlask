from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.learning_path import LearningPath
from app.utils.decorators import admin_required
from app import db

learning_path_bp = Blueprint('learning_path_bp', __name__)

@learning_path_bp.route('/trilhas', methods=['POST'])
@jwt_required()
@admin_required
def create_learning_path():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_path = LearningPath(name=name, description=description)
    db.session.add(new_path)
    db.session.commit()

    return jsonify({"msg": "Trilha de aprendizado criada"}), 201

@learning_path_bp.route('/trilhas', methods=['GET'])
@jwt_required()
def get_learning_paths():
    paths = LearningPath.query.all()

    response = []
    for path in paths:
        response.append({
            'id': path.id,
            'name': path.name,
            'description': path.description
        })

    return jsonify(response), 200


@learning_path_bp.route('/trilha/<int:learning_path_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_learning_path(learning_path_id):
    path = LearningPath.query.get_or_404(learning_path_id)
    path.delete()

    return jsonify({"msg": "Trilha deletada"}), 200