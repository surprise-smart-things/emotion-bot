from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/record')
def record():
    directory = os.path.join(app.root_path, 'videos')
    return render_template('record.html')


if __name__ == '__main__':
    app.run(debug=True)