from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    lessons = db.relationship('Lesson', backref='course', lazy=True)
    learning_paths = db.relationship('LearningPath', secondary='learning_path_courses', back_populates='courses')

    def delete(self):
        db.session.delete(self)
        db.session.commit()