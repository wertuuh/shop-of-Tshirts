from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User
from forms import RegisterForm

bp_main = Blueprint('main', __name__)

@bp_main.route("/")
def index():
    return render_template("index.html")

@bp_main.route("/card-one")
def card_one():
    return render_template("cardOne.html")

@bp_main.route("/card-two")
def card_two():
    return render_template("cardTwo.html")

@bp_main.route("/card-three")
def card_three():
    return render_template("cardThree.html")

@bp_main.route("/card-four")
def card_four():
    return render_template("cardFour.html")

@bp_main.route("/card-five")
def card_five():
    return render_template("cardFive.html")

@bp_main.route("/card-six")
def card_six():
    return render_template("cardSix.html")

@bp_main.route("/card-seven")
def card_seven():
    return render_template("cardSeven.html")

@bp_main.route("/card-eight")
def card_eight():
    return render_template("cardEight.html")

@bp_main.route("/card-nine")
def card_nine():
    return render_template("cardNine.html")

@bp_main.route("/card-ten")
def card_ten():
    return render_template("cardTen.html")

@bp_main.route("/card-eleven")
def card_eleven():
    return render_template("cardEleven.html")

@bp_main.route("/card-twelve")
def card_twelve():
    return render_template("cardTwelve.html")

@bp_main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("Этот email уже зарегистрирован")
        else:
            flash("Успешная регистрация!")
            return redirect(url_for("main.index"))

    return render_template("register.html", form=form)