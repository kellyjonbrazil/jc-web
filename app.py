#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import importlib
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from jc.cli import info as jc_info
from jc.cli import about_jc

TITLE = 'jc web'
DEBUG = False

app = Flask(__name__)

if os.getenv('APP_KEY'):
    app.config['SECRET_KEY'] = os.getenv('APP_KEY')
    print('Using production key', file=sys.stderr)
else:
    app.config['SECRET_KEY'] = 'deadbeef'
    print('Using development key', file=sys.stderr)

# convert parser list names to module names
parser_mod_list = []
for parser in about_jc()['parsers']:
    # do not include streaming parsers
    if not parser.get('streaming', None):
        parser_mod_list.append(parser['name'])


# --- ROUTES ---


@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyInput()
    output = ''
    if form.validate_on_submit():
        try:
            parser = importlib.import_module('jc.parsers.' + form.command_parser.data)
            output = parser.parse(form.command_output.data, quiet=True, raw=form.raw_json.data)
        except Exception:
            flash('jc was unable to parse the content. Did you use the correct parser?', 'danger')
            return render_template('home.html', title=TITLE, jc_info=jc_info, form=form, output=output)

        if form.pretty_print.data:
            output = json.dumps(output, indent=2)
        else:
            output = json.dumps(output)
        output = highlight(output, JsonLexer(), HtmlFormatter(noclasses=True))

    return render_template('home.html', title=TITLE, jc_info=jc_info, form=form, output=output)


# --- FORMS ---


class MyInput(FlaskForm):
    command_parser = SelectField('Parser', choices=parser_mod_list)
    command_output = TextAreaField('Command Output', validators=[DataRequired()])
    pretty_print = BooleanField('Pretty Print', default='checked')
    raw_json = BooleanField('Raw JSON')
    submit = SubmitField('Convert to JSON')


if __name__ == '__main__':
    app.run(debug=DEBUG)
