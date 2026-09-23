from flask import Blueprint, render_template

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