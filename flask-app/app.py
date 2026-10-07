import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from extensions import db
import models  # нужен, чтобы SQLAlchemy узнала о модели User
from routes import bp_main

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")

db.init_app(app)
CSRFProtect(app)
app.register_blueprint(bp_main)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8080)