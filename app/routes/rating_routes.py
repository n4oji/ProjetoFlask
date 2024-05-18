from flask import Blueprint, request, jsonify
from app.models.rating import Rating
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required
from app import db

rating_bp = Blueprint('rating_bp', __name__)

@rating_bp.route('/notas', methods=['POST'])
@jwt_required()
@admin_required
def create_rating():
    data = request.get_json()
    rating = data.get('rating')
    user_id = data.get('user_id')
    lesson_id = data.get('lesson_id')

    new_rating = Rating(rating=rating, user_id=user_id, lesson_id=lesson_id)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"msg": "Nota criada"}), 201


@rating_bp.route('/notas/<int:lesson_id>', methods=['GET'])
@jwt_required()
def get_ratings(lesson_id):
    try:
        ratings = Rating.query.filter_by(lesson_id=lesson_id).all()
    except:
        return jsonify({"msg": "Erro ao buscar as notas"}), 500

    response = []
    for rating in ratings:
        response.append({
            'rating': rating.rating,
            'user_id': rating.user_id,
            'lesson_id': rating.lesson_id
        })

    return jsonify(response), 200


@rating_bp.route('/notas/<int:rating_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    rating.delete()

    return jsonify({"msg": "Nota deletada"}), 200