from flask import Blueprint, render_template, redirect
from database.db import items
from bson.objectid import ObjectId

admin_bp = Blueprint('admin', __name__)

# Admin Dashboard
@admin_bp.route("/admin")
def admin_dashboard():
    all_items = list(items.find())
    return render_template("admin.html", items=all_items)


# Approve Claim
@admin_bp.route("/approve/<item_id>")
def approve(item_id):
    items.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"claimed": True}}
    )

    return redirect("/admin")