from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    print("Hello World from server")
    return "Hello World"


if __name__ == '__main__':
    print(30*"*", "|| Starting server ||", 30*"*")
    app.run(host='127.0.0.1', port=5000, debug=True)
