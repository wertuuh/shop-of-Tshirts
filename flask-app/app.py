from flask import Flask
from routes import bp_main

app = Flask(__name__)
app.register_blueprint(bp_main)

if __name__ == "__main__":
    app.run(debug=True, port=8080)