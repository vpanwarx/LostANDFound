import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.db import users

users.insert_one({"name": "test user"})
print("✅ MongoDB working!")