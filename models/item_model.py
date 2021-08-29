from db import db
from . import store_model

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) # us dollars goes to hundredths
    description = db.Column(db.String(280))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id, description=None):
        self.name = name
        self.price = price
        self.store_id = store_id
        if description is None:
            self.description = ""
        else:
            self.description = description

    def json(self):
        return {'name': self.name, 'price': self.price, 'description': self.description, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name

    # upserting (updating, inserting)
    def save_to_db(self):
        # session is the collection of objects to add to the database (only 1 in this case)
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.delete(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
