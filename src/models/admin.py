from ..utils import db
from enum import Enum

class Admin(db.Model):
    __tablename__='administrator'
    id=db.Column(db.Integer(), primary_key=True)
    adminName=db.Column(db.String(), nullable=False)
    userId=db.Column(db.String(), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>" 
    


    def save(self):
        db.session.add(self)
        db.session.commit()