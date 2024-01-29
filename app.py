from flask import Flask, jsonify, request, render_template
from modules.basic_message_analysis import basic_analysis_page, analyze_message_content, messages, Message, \
    generate_message_html

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
    app.run(host="192.168.1.41", port=443, ssl_context=(certfile, keyfile))
