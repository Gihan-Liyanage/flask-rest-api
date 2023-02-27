from ..utils import db
from enum import Enum

class UserTypes(Enum):
    ADMIN = 'admin'
    INSTRUCTOR = 'instructor'
    STUDENT = 'student'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    passwordhash = db.Column(db.Text(), nullable=False)
    usertype = db.Column(db.Enum(UserTypes), default=UserTypes.INSTRUCTOR)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
