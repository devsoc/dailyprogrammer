import os
import ast
import queue
import asyncio
import threading

from boto.s3.key import Key
from boto.s3.connection import S3Connection

import settings
from score import get_names
from flask import Flask, render_template

app = Flask(__name__)
s3 = S3Connection(settings.AWS_KEY, settings.AWS_SECRET)

def update_cache():
    api_url = 'https://api.github.com'
    url = api_url + '/repos/devsoc/dailyprogrammer/contents/solutions'
    loop = asyncio.new_event_loop()
    Q = queue.Queue()

    def wrapper():
        Q.put(loop.run_until_complete(get_names(loop, url)))
    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join()

    bucket = s3.get_bucket('dp-score-cache')
    k = Key(bucket)
    k.key = 'scores'
    k.set_contents_from_string(str(Q.get()))


def get_cache():
    bucket = s3.get_bucket('dp-score-cache')
    k = Key(bucket)
    k.key = 'scores'
    return ast.literal_eval(k.get_contents_as_string().decode())


@app.route('/')
def home():
    return render_template('score.html', data=get_cache())


@app.route('/update')
def update():
    update_cache()
    return 'done!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
