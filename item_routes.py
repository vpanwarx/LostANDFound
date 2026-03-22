print("✅ item_routes loaded")

from flask import Blueprint, render_template, request, redirect
from database.db import items
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os

item_bp = Blueprint('items', __name__)

UPLOAD_FOLDER = "uploads"

# 🏠 Home
@item_bp.route("/")
def home():
    all_items = list(items.find())
    return render_template("index.html", items=all_items)


# 🔴 Lost Filter
@item_bp.route("/lost_items")
def lost_items():
    data = list(items.find({"status": "lost"}))
    return render_template("index.html", items=data)


# 🟢 Found Filter
@item_bp.route("/found_items")
def found_items():
    data = list(items.find({"status": "found"}))
    return render_template("index.html", items=data)


# 🔍 Search
@item_bp.route("/search", methods=["POST"])
def search():
    query = request.form["query"]

    results = list(items.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"location": {"$regex": query, "$options": "i"}}
        ]
    }))

    return render_template("index.html", items=results)


# 🔴 Report Lost
@item_bp.route("/report_lost", methods=["GET", "POST"])
def report_lost():
    if request.method == "POST":

        file = request.files["image"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        items.insert_one({
            "title": request.form["title"],
            "description": request.form["description"],
            "location": request.form["location"],
            "status": "lost",
            "image": filename,
            "claimed": False,
            "claim_requests": []
        })

        return redirect("/")

    return render_template("report_lost.html")


# 🟢 Report Found
@item_bp.route("/report_found", methods=["GET", "POST"])
def report_found():
    if request.method == "POST":

        file = request.files["image"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        items.insert_one({
            "title": request.form["title"],
            "description": request.form["description"],
            "location": request.form["location"],
            "status": "found",
            "image": filename,
            "claimed": False,
            "claim_requests": []
        })

        return redirect("/")

    return render_template("report_found.html")


# ⭐ Claim Item
@item_bp.route("/claim/<item_id>", methods=["GET", "POST"])
def claim_item(item_id):
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        items.update_one(
            {"_id": ObjectId(item_id)},
            {
                "$push": {
                    "claim_requests": {
                        "name": name,
                        "message": message
                    }
                }
            }
        )

        return redirect("/")

    return render_template("claim.html", item_id=item_id)