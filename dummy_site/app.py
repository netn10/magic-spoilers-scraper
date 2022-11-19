import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def site():
    return render_template('site.html')

@app.route('/static_test')
def static_test():
    return render_template('static_test.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
