from flask import Flask
from routes.package_routes import package_bp

app = Flask(__name__)

# register blueprint
app.register_blueprint(package_bp)

# optional root (to avoid 404 confusion)
@app.route('/')
def home():
    return "API is running"

if __name__ == "__main__":
    app.run(debug=True)