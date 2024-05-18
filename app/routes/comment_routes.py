from flask import Blueprint, request, jsonify
from app.models.comment import Comment
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required
from app import db

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/comentarios', methods=['POST'])
@jwt_required()
@admin_required
def create_comment():
    data = request.get_json()
    content = data.get('content')
    user_id = data.get('user_id')
    lesson_id = data.get('lesson_id')

    new_comment = Comment(content=content, user_id=user_id, lesson_id=lesson_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"msg": "Comentário criado"}), 201


@comment_bp.route('/comentarios/<int:lesson_id>', methods=['GET'])
@jwt_required()
def get_comments(lesson_id):
    try:
        comments = Comment.query.filter_by(lesson_id=lesson_id).all()
    except:
        return jsonify({"msg": "Erro ao buscar os comentários"}), 500
    response = []
    for comment in comments:
        response.append({
            'content': comment.content,
            'user_id': comment.user_id,
            'lesson_id': comment.lesson_id
        })

    return jsonify(response), 200

@comment_bp.route('/comentarios/<int:comment_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.delete()

    return jsonify({"msg": "Comentário deletado"}), 200

