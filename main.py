from flask import Flask, escape, request
from flask_basicauth import BasicAuth
from gevent.pywsgi import WSGIServer
import secret

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = secret.USERNAME
app.config['BASIC_AUTH_PASSWORD'] = secret.PASSWORD
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


if __name__ == '__main__':
    http_server = WSGIServer(('', 6974), app)
    http_server.serve_forever()