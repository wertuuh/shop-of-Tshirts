from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User
from forms import RegisterForm
from products import PRODUCTS, SIZES
 
bp_main = Blueprint('main', __name__)
 
 
# ---------------------- Корзина (хранится в session) ----------------------
# Ключ позиции: "<id товара>:<размер>", значение — количество.
def _cart():
    return session.setdefault("cart", {})
 
 
def _size_qty_map(product_id):
    """Количество в корзине по каждому размеру для одного товара —
    передаётся на страницу карточки, чтобы сразу показать правильную
    кнопку (Добавить / В корзине: N)."""
    cart = _cart()
    return {size: cart.get(f"{product_id}:{size}", 0) for size in SIZES}
 
 
def _cart_total():
    total = 0
    for key, qty in _cart().items():
        pid, _, _size = key.partition(":")
        product = PRODUCTS.get(int(pid))
        if product:
            total += product["price"] * qty
    return total
 
 
def _wants_json():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"
 
 
@bp_main.app_context_processor
def inject_cart_count():
    return {"cart_count": sum(_cart().values())}
 
 
@bp_main.app_template_filter("rub")
def rub(value):
    return f"{value:,}".replace(",", " ")
 
 
@bp_main.route("/")
def index():
    search_items = [{"name": p["name"], "url": url_for(p["endpoint"])} for p in PRODUCTS.values()]
    return render_template("index.html", search_items=search_items)
 
@bp_main.route("/card-one")
def card_one():
    return render_template("cardOne.html", cart_qty=_size_qty_map(1))
 
@bp_main.route("/card-two")
def card_two():
    return render_template("cardTwo.html", cart_qty=_size_qty_map(2))
 
@bp_main.route("/card-three")
def card_three():
    return render_template("cardThree.html", cart_qty=_size_qty_map(3))
 
@bp_main.route("/card-four")
def card_four():
    return render_template("cardFour.html", cart_qty=_size_qty_map(4))
 
@bp_main.route("/card-five")
def card_five():
    return render_template("cardFive.html", cart_qty=_size_qty_map(5))
 
@bp_main.route("/card-six")
def card_six():
    return render_template("cardSix.html", cart_qty=_size_qty_map(6))
 
@bp_main.route("/card-seven")
def card_seven():
    return render_template("cardSeven.html", cart_qty=_size_qty_map(7))
 
@bp_main.route("/card-eight")
def card_eight():
    return render_template("cardEight.html", cart_qty=_size_qty_map(8))
 
@bp_main.route("/card-nine")
def card_nine():
    return render_template("cardNine.html", cart_qty=_size_qty_map(9))
 
@bp_main.route("/card-ten")
def card_ten():
    return render_template("cardTen.html", cart_qty=_size_qty_map(10))
 
@bp_main.route("/card-eleven")
def card_eleven():
    return render_template("cardEleven.html", cart_qty=_size_qty_map(11))
 
@bp_main.route("/card-twelve")
def card_twelve():
    return render_template("cardTwelve.html", cart_qty=_size_qty_map(12))
 
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
 
 
@bp_main.route("/cart")
def cart():
    items, total = [], 0
    for key, qty in _cart().items():
        pid, _, size = key.partition(":")
        product = PRODUCTS.get(int(pid))
        if not product:
            continue
        subtotal = product["price"] * qty
        total += subtotal
        items.append({"id": int(pid), "size": size, "qty": qty, "subtotal": subtotal, **product})
    return render_template("cart.html", items=items, total=total)
 
 
@bp_main.route("/cart/add/<int:product_id>", methods=["POST"])
def cart_add(product_id):
    size = request.form.get("size", "")
    if product_id not in PRODUCTS or size not in SIZES:
        if _wants_json():
            return jsonify(ok=False, error="invalid"), 400
        flash("Не удалось добавить товар")
        return redirect(url_for("main.index"))
 
    cart = _cart()
    key = f"{product_id}:{size}"
    cart[key] = min(cart.get(key, 0) + 1, 99)
    session.modified = True
 
    if _wants_json():
        return jsonify(ok=True, qty=cart[key], cart_count=sum(_cart().values()), total=_cart_total())
 
    flash(f"Добавлено в корзину: {PRODUCTS[product_id]['name']}, размер {size}")
    return redirect(url_for(PRODUCTS[product_id]["endpoint"]))
 
 
@bp_main.route("/cart/update/<int:product_id>/<size>", methods=["POST"])
def cart_update(product_id, size):
    cart = _cart()
    key = f"{product_id}:{size}"
    if key in cart:
        cart[key] += 1 if request.form.get("action") == "inc" else -1
        if cart[key] <= 0:
            del cart[key]
        else:
            cart[key] = min(cart[key], 99)
        session.modified = True
 
    if _wants_json():
        qty = cart.get(key, 0)
        product = PRODUCTS.get(product_id)
        subtotal = product["price"] * qty if product else 0
        return jsonify(
            ok=True,
            qty=qty,
            subtotal=subtotal,
            cart_count=sum(cart.values()),
            total=_cart_total(),
        )
 
    return redirect(url_for("main.cart"))
 
 
@bp_main.route("/cart/remove/<int:product_id>/<size>", methods=["POST"])
def cart_remove(product_id, size):
    _cart().pop(f"{product_id}:{size}", None)
    session.modified = True
 
    if _wants_json():
        return jsonify(ok=True, cart_count=sum(_cart().values()), total=_cart_total())
 
    return redirect(url_for("main.cart"))
 
 
@bp_main.route("/cart/clear", methods=["POST"])
def cart_clear():
    session.pop("cart", None)
 
    if _wants_json():
        return jsonify(ok=True, cart_count=0, total=0)
 
    return redirect(url_for("main.cart"))