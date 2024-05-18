from app import db

class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    courses = db.relationship('Course', secondary='learning_path_courses', back_populates='learning_paths')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LearningPathCourses(db.Model):
    __tablename__ = 'learning_path_courses'
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_path.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)