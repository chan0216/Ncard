from flask import *
from api.newpost import newpost_blueprint
from api.user import user_blueprint
from api.profile import profile_blueprint
from flask_mail import Mail, Message
from decouple import config


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(newpost_blueprint)
    app.register_blueprint(profile_blueprint)
    app.config["JSON_AS_ASCII"] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def signin():
    return render_template("login.html")


@app.route("/unconfirmed")
def unconfirmed():
    return render_template("unconfirmed.html")


@app.route("/confirmed")
def confirmed():
    return render_template("confirmed.html")


@app.route("/verify/school")
def verifyschool():
    return render_template("profile.html")


@app.route("/new-post")
def newpost():
    return render_template("newpost.html")


if __name__ == "__main__":
    app.run(port=80, debug=True)
