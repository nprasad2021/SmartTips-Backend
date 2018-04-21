from app import db
from app.models import *

def seed_db():
    db.create_all()
    for i in range(5):
        user = User('Foo{}'.format(i), 'Bar{}'.format(i))
        db.session.add(user)
    db.session.commit()

