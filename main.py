from flask import Flask, escape, request
from flask_basicauth import BasicAuth
from gevent.pywsgi import WSGIServer
import secret

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = secret.USERNAME
app.config['BASIC_AUTH_PASSWORD'] = secret.PASSWORD
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


import index 

app.route('/')(index.mainpage)
app.route('/favicon.ico')(index.favicon)


if __name__ == '__main__':
    http_server = WSGIServer(('', 6974), app)
    http_server.serve_forever()