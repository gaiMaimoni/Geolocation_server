#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def get_hello():
    return ''

if __name__ == '__main__':
    from sys import argv

    _port = 8080
    _host = '127.0.0.1'
    if len(argv) >= 2:
        _port=int(argv[1])
    if len(argv) >= 3:
        _host=argv[2]

    app.run(debug=True,port=_port, host=_host)