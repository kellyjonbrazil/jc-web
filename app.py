#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets
import importlib
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

TITLE = 'jc web'
DEBUG = True

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

parsers = [
    'airport',
    'airport_s',
    'arp',
    'blkid',
    'crontab',
    'crontab_u',
    'csv',
    'date',
    'df',
    'dig',
    'dmidecode',
    'du',
    'env',
    'file',
    'free',
    'fstab',
    'group',
    'gshadow',
    'history',
    'hosts',
    'id',
    'ifconfig',
    'ini',
    'iptables',
    'jobs',
    'kv',
    'last',
    'ls',
    'lsblk',
    'lsmod',
    'lsof',
    'mount',
    'netstat',
    'ntpq',
    'passwd',
    'ping',
    'pip_list',
    'pip_show',
    'ps',
    'route',
    'shadow',
    'ss',
    'stat',
    'sysctl',
    'systemctl',
    'systemctl_lj',
    'systemctl_ls',
    'systemctl_luf',
    'timedatectl',
    'tracepath',
    'traceroute',
    'uname',
    'uptime',
    'w',
    'who',
    'xml',
    'yaml'
]

# --- ROUTES ---


@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyInput()
    output = 'JSON Conversion'
    if form.validate_on_submit():
        try:
            parser = importlib.import_module('jc.parsers.' + form.command_parser.data)
            output = parser.parse(form.command_output.data, quiet=True)
        except Exception:
            flash('jc was unable to parse the content. Did you use the correct parser?', 'danger')
            return redirect(url_for('home'))
        if form.pretty_print.data:
            output = json.dumps(output, indent=2)
        else:
            output = json.dumps(output)
        output = highlight(output, JsonLexer(), HtmlFormatter(noclasses=True))
    return render_template('home.html', title=TITLE, form=form, output=output)


# --- FORMS ---


class MyInput(FlaskForm):
    command_parser = SelectField('Parser', choices=parsers)
    command_output = TextAreaField('Command Output', validators=[DataRequired()])
    pretty_print = BooleanField('Pretty Print', default='checked')
    submit = SubmitField('Convert to JSON')


if __name__ == '__main__':
    app.run(debug=DEBUG)
