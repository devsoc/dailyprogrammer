import os
import queue
import asyncio
import threading

from score import get_names
from flask import Flask, render_template

app = Flask(__name__)


def generate_output():
    api_url = 'https://api.github.com'
    url = api_url + '/repos/devsoc/dailyprogrammer/contents/solutions'
    loop = asyncio.new_event_loop()

    Q = queue.Queue()
    def wrapper():
        Q.put(loop.run_until_complete(get_names(loop, url)))
    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join()
    return Q


@app.route('/')
def home():
    return render_template('score.html', data=generate_output().get())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
