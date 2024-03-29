#!/usr/bin/env python3
# coding: utf-8

import os

from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.seed_db import *
from api import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    "Add seed data to the database."
    seed_db()

if __name__ == "__main__":
    manager.run()
