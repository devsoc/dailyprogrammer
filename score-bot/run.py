import os
import asyncio
import threading

from score import main
from flask import Flask

app = Flask(__name__)


def run_script():
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_until_complete(main(loop)))
    thread.start()
    thread.join()


@app.route('/', methods=['GET', 'POST'])
def home():
    run_script()
    return 'Done'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
