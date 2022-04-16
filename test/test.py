from flask import Flask
from flask import request, render_template

app = Flask(__name__)


@app.route('/')
def root():
    return "hello"


@app.route("/login1")
def login1():
    name = request.values.get("name")
    passwd = request.values.get("passwd")
    return f'name={name},passwd={passwd}'


@app.route('/login')
def login():
    return """
    <form action='/login1'>
        账号:<input name = 'name'><br>
        密码:<input name = 'passwd'><br>
        <input type = "submit">
    </form>
    """


@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/ajax", methods=['get', 'post'])
def ajax():
    return '100'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
