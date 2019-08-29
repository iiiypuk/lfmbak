#!/usr/bin/env python3

import json
from flask import Flask, escape, request, render_template, send_from_directory
import lastfm_backup as lfm

def backup(USERNAME):
    API_KEY = '0'
    pages = lfm.get_pages(USERNAME, API_KEY)
    count = 0
    data = []

    for page in range(1, pages + 1):
        tracks = lfm.get_scrobbles(USERNAME, API_KEY, page)

        for track in tracks:
            data.append({'artist': track['artist']['#text'],
                           'name': track['name'],
                           'album': track['album']['#text'],
                           'date': track['date']['uts']})
            count = count + 1

    with open('./data/%s.json' % (USERNAME), 'w+', encoding='utf-8') as f:
        f.write(
            json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))

    return ('%s.json' % (USERNAME), count)

app = Flask(__name__)

@app.route('/')
def lfmbakweb():
    name = request.args.get("user_name", "XUY")
    return render_template('index.html', name = name)

@app.route('/bak', methods=['GET'])
def bak():
    name = request.args.get("user_name")
    file, count = backup(name)
    return render_template('bak.html', filename=file, count=count)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('./data/', filename)
