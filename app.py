from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

from modules.basic_message_analysis import basic_analysis_page

certfile = r'C:/Certbot/archive/silmat-auki.com/cert1.pem'
keyfile = r'C:/Certbot/archive/silmat-auki.com/privkey1.pem'
app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('html-pages/index.html')


@app.route('/basic_analysis', methods=['GET', 'POST'])
def basic():
    return basic_analysis_page()


@app.route('/trigram_analysis')
def trigram():
    return render_template('html-pages/trigram_message_analysis.html')


@app.route('/isochain_analysis')
def isochain():
    return render_template('html-pages/isochain_message_analysis.html')


if __name__ == '__main__':
    app.run(host="192.168.1.41", port=80)
    # http_server = WSGIServer(('192.168.1.41', 443), app, keyfile=keyfile, certfile=certfile)
    # http_server.serve_forever()
