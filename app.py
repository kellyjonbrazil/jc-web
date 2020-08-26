#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField
from wtforms.validators import DataRequired

DEBUG = True
TITLE = 'jc web'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

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
def index():
    form = MyInput()
    output = ''
    if form.validate_on_submit():
        parser = importlib.import_module('jc.parsers.' + form.command_parser.data)
        output = parser.parse(form.command_output.data)
        output = json.dumps(output, indent=2)
    return render_template('index.html', title=TITLE, form=form, output=output)


# --- FORMS ---


class MyInput(FlaskForm):
    command_parser = SelectField('Parser', choices=parsers)
    command_output = TextAreaField('Command Output', validators=[DataRequired()])


if __name__ == '__main__':
    app.run(debug=DEBUG)
