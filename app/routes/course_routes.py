from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.course import Course
from app.utils.decorators import admin_required
from app import db

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/cursos', methods=['POST'])
@admin_required
@jwt_required()
def create_course():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_course = Course(name=name, description=description)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"msg": "Curso criado"}), 201

@course_bp.route('/cursos/<int:course_id>', methods=['DELETE'])
@admin_required
@jwt_required()
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    course.delete()

    return jsonify({"msg": "Curso Deletado"}), 200

@course_bp.route('/cursos', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    response = []   
    for course in courses:
        response.append({
            'id': course.id,
            'name': course.name,
            'description': course.description
        })

    return jsonify(response), 200    

@course_bp.route('/cursos/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    lessons = [
        {
            'name': lesson.name,
            'id': lesson.id
        }
        for lesson in course.lessons
    ]
    response = {
        'id': course.id,
        'name': course.name,
        'description': course.description
    }   
    response['lessons'] = lessons

    return jsonify(response), 200  

