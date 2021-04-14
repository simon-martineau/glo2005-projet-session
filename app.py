from conf import BasicConfig
from flask import Flask

app = Flask(__name__)

app.config.update(BasicConfig)  # TODO: Requires dict maybe?

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
