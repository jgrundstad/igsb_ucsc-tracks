__author__ = 'jgrundst'
from flask import Flask, request, render_template
import os
templ_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=templ_dir)


@app.route("/")
def hello():
    return render_template('/echo.html')


@app.route("/echo", methods=['POST'])
def echo():
    return "You said: " + request.form['text']


if __name__ == "__main__":
    app.run(debug=True)