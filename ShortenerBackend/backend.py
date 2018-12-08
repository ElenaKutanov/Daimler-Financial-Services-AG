#! /usr/bin/env python

import sqlite3
from sqlite3 import IntegrityError
import validators
import json
from random import random, choice
from contextlib import closing

from flask import Flask, render_template, g, redirect, request, jsonify
from flask_cors import CORS, cross_origin



DATABASE = 'Database.db'

invalid = 422
ok = 200

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def index():
    if request.method == 'POST':
        req = request.json
        url = req['url']
        desired_slug = req['desired_slug']
        # TODO, self create
        if validators.url(url):
            if len(desired_slug) > 0:
               if validators.url('http://test.com/' + desired_slug) and len(desired_slug) > 6:
                    return jsonify({'message': 'The desired url has invalid symbols or length larger than 6 symbols'}), 400
               result = save_to_db(url, desired_slug)
               if result:
                   return jsonify({'slug': desired_slug, 'message': 'success'}), ok
               else:
                    return jsonify({'message': 'This short url is already have taken'}), 400
            else:
                slug = None
                while True:
                    slug = create_slug()
                    result = save_to_db(url, slug)
                    if result:
                        break
                return jsonify({'slug': slug, 'message': 'success'}), ok
        else:
            return jsonify({'message': 'The url is invalid'}), invalid

@app.route('/<slug>')
@cross_origin(supports_credentials=True)
def redirect_request(slug):
    print(slug)
    url = g.db.execute('''SELECT url FROM urls WHERE slug = ?''', [slug]).fetchone()
    print(url);
    if not url:
        return 'Not found!', 404
    return redirect(url[0], code=302 )


def save_to_db(url, slug):
    result = False
    try:
        g.db.execute('''INSERT INTO urls(url, slug) VALUES(?, ?);''', [url, slug])
        g.db.commit()
        result = True
    except IntegrityError as err:
        pass
    return result


def create_slug():
    url_safe_symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-_~!+,*:@"
    max_chars = 6 # TODO, max number
    return ''.join([choice(url_safe_symbols) for _ in range(max_chars)])

if __name__ == '__main__':
    app.run()
