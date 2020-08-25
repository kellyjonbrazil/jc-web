#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

DEBUG = True
TITLE = 'jc web'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title=TITLE)


if __name__ == '__main__':
    app.run(debug=DEBUG)
