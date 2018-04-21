from app import db
from app.models import *

def seed_db():
    db.drop_all()
    db.create_all()
    create_fake_users()
    create_fake_places()

def create_fake_users():
    user = User('Mikhail', 'Maslo',
         'https://avatars1.githubusercontent.com/u/15061918?s=400&v=4')
    user.api_token = 'uwfbT3DYE1sQ3cHQf_ym-B4--qcQJu-PHu7GpuDXbdI'
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
