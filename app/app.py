from flask import Flask, render_template
import nasa

app = Flask(__name__)
data = nasa.format()


@app.route("/")
def index():
    return render_template("index.html", space_list=data, title="AstroDodge")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/list")
def space_list():
    return render_template("list.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
