from app import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    comments = db.relationship('Comment', backref='lesson', lazy=True)
    ratings = db.relationship('Rating', backref='lesson', lazy=True)

    def delete(self):
        db.session.delete(self)
        db.session.commit()