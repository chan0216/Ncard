from flask import *
import model.main
import controller.decorator as dec

pages = Blueprint("pages", __name__)


@pages.route("/")
def index():
    return render_template("index.html")


@pages .route("/login")
def signin():
    return render_template("login.html")


@pages.route("/verify/school")
def verify_school():
    return render_template("verify.html")


@pages.route("/new-post")
def newpost():
    return render_template("newpost.html")


@pages.route("/member")
def member():
    return render_template("member.html")


@pages.route("/my/profile")
def myprofile():
    return render_template("cardprofile.html")


@pages.route("/ncard")
def ncard():
    return render_template("ncard.html")


@pages.route("/my/friends")
def friends():
    return render_template("friends.html")


@pages.route("/post/<id>")
def attraction(id):
    return render_template("post.html")


@pages.route("/friend/<id>")
def get_friend_data(id):
    return render_template("mate.html")


@pages.route('/chats', methods=['GET'])
@dec.token_required
def redirect_msg(current_user):
    resp = model.main.redirect_msg(current_user)
    if resp:
        ncardid = resp[0]
        return redirect(url_for('pages.chats', id=ncardid))
    return redirect(url_for('pages.chats'))


@pages.route("/chats/<id>")
@pages.route("/chats/", defaults={'id': None})
def chats(id):
    if id:
        return render_template("chats.html")
    else:
        return render_template("nochats.html")
