#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import mistune
from pygments import highlight
from pygments.lexers import JsonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SelectField, BooleanField, SubmitField
from jc import __version__, standard_parser_mod_list, parse, parser_info


TITLE = 'jc web'
DEBUG = False

app = Flask(__name__)

if os.getenv('APP_KEY'):
    app.config['SECRET_KEY'] = os.getenv('APP_KEY')
    print('Using production key', file=sys.stderr)
else:
    app.config['SECRET_KEY'] = 'deadbeef'
    print('Using development key', file=sys.stderr)


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(noclasses=True)
            return highlight(code, lexer, formatter)
        return '<div style="background-color: #f8f8f8;"><pre>' + mistune.escape(code[:-1]) + '</pre></div>'

    def block_quote(self, text):
        return '<blockquote class="alert alert-warning pb-0">' + text + '</blockquote>'


# --- ROUTES ---


@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyInput()
    output = ''
    if form.validate_on_submit():
        try:
            output = parse(form.command_parser.data,
                           form.command_output.data,
                           quiet=True,
                           raw=form.raw_json.data)
        except Exception:
            flash('jc was unable to parse the content. Did you use the correct parser?', 'danger')
            return render_template('home.html',
                                   title=TITLE,
                                   jc_version=__version__,
                                   form=form,
                                   output=output)

        if form.pretty_print.data:
            output = json.dumps(output, indent=2)
        else:
            output = json.dumps(output)
        output = highlight(output, JsonLexer(), HtmlFormatter(noclasses=True))

    return render_template('home.html',
                           title=TITLE,
                           jc_version=__version__,
                           form=form,
                           output=output)


@app.route('/parserdoc', methods=(['POST']))
def parser_doc():
    form = MyInput()
    p_info = ''
    md = mistune.create_markdown(renderer=HighlightRenderer())

    if form.validate_on_submit():
        p_info = parser_info(form.command_parser.data, documentation=True)
        markdown_doc = md(p_info.get('documentation', ''))
        markdown_desc = md(p_info.get('description', ''))
        markdown_desc = markdown_desc.replace('<p>', '').replace('</p>', '')

    return render_template('parserdoc.html',
                           title=f'{TITLE} - {p_info.get("name", "")} documentation',
                           jc_version=__version__,
                           p_info=p_info,
                           description=markdown_desc,
                           documentation=markdown_doc)

# --- FORMS ---


class MyInput(FlaskForm):
    command_parser = SelectField('Parser', choices=standard_parser_mod_list())
    command_output = TextAreaField('Command Output')
    pretty_print = BooleanField('Pretty Print', default='checked')
    raw_json = BooleanField('Raw JSON')
    parserdoc = SubmitField('Get Parser Documentation')
    submit = SubmitField('Convert to JSON')


if __name__ == '__main__':
    app.run(debug=DEBUG)
