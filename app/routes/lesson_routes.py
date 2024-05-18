from flask import Blueprint, request, jsonify
from app.models.lesson import Lesson
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required
from app import db

lesson_bp = Blueprint('lesson_bp', __name__)

@lesson_bp.route('/aulas', methods=['POST'])
@jwt_required()
@admin_required
def create_lesson():
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    course_id = data.get('course_id')

    new_lesson = Lesson(name=name, content=content, course_id=course_id)
    db.session.add(new_lesson)
    db.session.commit()

    return jsonify({"msg": "Aula criada"}), 201


@lesson_bp.route('/aulas', methods=['GET'])
@jwt_required()
def get_lessons():
    lessons = Lesson.query.all()
    response = []
    for lesson in lessons:
        response.append({
            'name': lesson.name,
            'course_id': lesson.course_id
        })

    return jsonify([lesson.name for lesson in lessons]), 200

@lesson_bp.route('/aulas/<int:lesson_id>', methods=['GET'])
@jwt_required()
def get_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    response = {
        'name': lesson.name,
        'content': lesson.content,
        'course_id': lesson.course_id
    }

    return jsonify(response), 200

@lesson_bp.route('/aulas/<int:lesson_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    lesson.delete()

    return jsonify({"msg": "Aula deletada"}), 200