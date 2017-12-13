#!/usr/bin/python3
'''module: 0-hello_route
demonstrating basic flask functionality '''
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello, HBNB!'

if __name__ == '__main__':
    app.run()
