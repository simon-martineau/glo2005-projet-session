from conf import BasicConfig
from flask import Flask, render_template

app = Flask(__name__)

app.config.from_object(BasicConfig)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
