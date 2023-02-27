from enum import Enum

from ..utils import db

class Modules(str, Enum):
    IMAGE_PROCESSING='IMAGE_PROCESSING'
    VOICE_REC='VOICE_REC'
    FACE_DETECT='FACE_DETECT'

user_class = db.Table('user_class',
    db.Column('user_id', db.Integer,db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

class Class(db.Model):
    __tablename__='class'
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(), nullable=False)
    passwordhash=db.Column(db.Text(), nullable=False)
    module=db.Column(db.Enum(Modules), nullable=False)
    attending = db.relationship('User', secondary=user_class, backref='attndees')

    def __repr__(self) -> str:
        return f"<Class {self.name}>" 

    def save(self):
        db.session.add(self)
        db.session.commit()