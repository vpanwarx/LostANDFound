from flask import Flask, send_from_directory
from routes.auth_routes import auth_bp
from routes.item_routes import item_bp
from routes.admin_routes import admin_bp

# ✅ Create app FIRST
app = Flask(__name__)

app.secret_key = "secret123"

# ✅ Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(item_bp)
app.register_blueprint(admin_bp)

# ✅ THEN define routes
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)