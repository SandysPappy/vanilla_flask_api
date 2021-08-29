from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    # the python id function can be wonky using id here
    # primary keys are always autoincremented
    id = db.Column(db.Integer, primary_key=True)
    # the 80 limits size
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.something = "This is still in the object however will not be stored/read from the database"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # returns a user object if found
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
