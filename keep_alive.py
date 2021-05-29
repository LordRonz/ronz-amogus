from flask import Flask
from threading import Thread

class localFlask(Flask):
    def process_response(self, res):
        #Every response will be processed here first
        res.headers = {}
        return res

app = localFlask('')

@app.route('/')
def home():
    return ''

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()