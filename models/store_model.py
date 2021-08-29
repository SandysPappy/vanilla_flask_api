from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(280))

    # now, self.items is no longer a list of items. It is now
    # a query builder which can look into the items table
    # otherwise, everytime we create a Store, we would have to look into the table
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, description=None):
        self.name = name
        if description is None:
            self.description = ""
        else:
            self.description = description

    # For read-write speed, check out video 102 at time 10:10
    def json(self):
        # this line is if we didn't have lazy='dynamic'
        # return {'name': self.name, 'items': [item.json() for item in self.items], 'description': self.description}
        return {'name': self.name, 'items': [item.json() for item in self.items.all()], 'description': self.description}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name

    # upserting (updating, inserting)
    def save_to_db(self):
        # session is the collection of objects to add to the database (only 1 in this case)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
