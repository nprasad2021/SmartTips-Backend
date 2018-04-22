from app import db
from app.models import *
from random import shuffle, randint
import json
import requests

def seed_db():
    db.drop_all()
    db.create_all()
    create_fake_users()
    create_fake_places()
    create_fake_waiter()
    create_fake_tips()

def create_fake_waiter():
    place = Place.query.all()[0]
    waiter = Waiter(
        'Austin',
        'Powers',
        'http://screencrush.com/files/2017/04/Austin-Powers-goofy-teeth.jpg',
        place.id)
    db.session.add(waiter)
    db.session.commit()

def create_fake_users():
    user = User('Mikhail', 'Maslo',
         'https://avatars1.githubusercontent.com/u/15061918?s=400&v=4')
    user.api_token = 'uwfbT3DYE1sQ3cHQf_ym-B4--qcQJu-PHu7GpuDXbdI'
    db.session.add(user)
    db.session.commit()

def create_fake_places():
    chaihona = Place('Chaihona #1', 'Новослободская улица, 16',
            55.781760, 37.599056, 9, True)
    shokoladnica = Place('Shokoladnica', 'Новослободская улица, 9 стр 1',
            55.784606, 37.596588, 6, True)
    montana = Place('Lounge Cafe Montana', 'Новослободская улица, 10 корпус 2',
            55.780554, 37.600465, 7, True)
    yakitoriya = Place('Yakitoriya', 'Новослободская улица, 20',
            55.782174, 37.598753, 7, True)
    marukame = Place('Marukame', 'ул. Сущевская, 27, стр. 2',
            55.782871, 37.601134, 9, True)
    doublebi = Place('DoubleB', 'Новослободская улица, 18',
            55.782234, 37.599331, 8, True)
    dzhondzholi = Place('DzhonDzholi', 'Новослободская улица, 14/19с1',
            55.781069, 37.599635, 8, True)
    sosnailipa = Place('Sosna i Lipa', 'улица Покровка, 17',
            55.759471, 37.645537, 10, True)
    babetta = Place('Babetta', 'Мясницкая улица, 15',
            55.763121, 37.635053, 6, True)
    didi = Place('Didi', 'Тверской бульвар, 14, стр. 4',
            55.759800, 37.601517, 8, True)

    places = [chaihona, shokoladnica, montana, yakitoriya, marukame,
             doublebi, dzhondzholi, sosnailipa, babetta, didi]
    [db.session.add(p) for p in places]

    db.session.commit()

def create_fake_tips():
    users = []
    for i in range(1, 18):
        URL = 'https://randomuser.me/api/'
        data = requests.get(URL).json()
        user = User(
            data['results'][0]['name']['first'],
            data['results'][0]['name']['last'],
            data['results'][0]['picture']['medium']
        )
        users.append(user)
        db.session.add(user)

    places = Place.query.all()

    for user in users:
        for i in range(1, 5):
            shuffle(places)
            place_id = places[0].id
            random_amount = randint(100, 1000)
            random_rate = randint(4, 20)
            tip = Tip(place_id, user.id, random_amount, random_rate)
            db.session.add(tip)

    db.session.commit()
