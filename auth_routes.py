from flask import Blueprint, render_template, request, redirect, session
from database.db import users
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed
        })

        return redirect("/login")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            session["user"] = user["username"]
            return redirect("/dashboard")

    return render_template("login.html")