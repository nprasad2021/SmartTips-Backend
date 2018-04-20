# coding: utf-8

from . import main
from flask import render_template, current_app

@main.route('/')
def index():
    return render_template('index.html', app_config=current_app.config)

