from app import db
from app.models import *

def seed_db():
    db.create_all()
    for i in range(5):
        user = User('Foo{}'.format(i), 'Bar{}'.format(i))
        db.session.add(user)
    db.session.commit()


def create_fake_places():
    yakitoriya = Place('Yakitoriya', 'Новослободская улица, 20',
            55.782174, 37.598753, True)
    marukame = Place('Marukame', 'ул. Сущевская, 27, стр. 2',
            55.782871, 37.601134, True)
    doublebi = Place('DoubleB', 'Новослободская улица, 18',
            55.782234, 37.599331, True)
    dzhondzholi = Place('DzhonDzholi', 'Новослободская улица, 14/19с1',
            55.781069, 37.599635, True)
    sosnailipa = Place('Sosna i Lipa', 'улица Покровка, 17',
            55.759471, 37.645537, True)
    babetta = Place('Babetta', 'Мясницкая улица, 15',
            55.763121, 37.635053, True)
    didi = Place('Didi', 'Тверской бульвар, 14, стр. 4',
            55.759800, 37.601517, True)

    places = [ yakitoriya, marukame, doublebi, dzhondzholi, sosnailipa, babetta, didi]
    [db.session.add(p) for p in places]

    db.session.commit()
