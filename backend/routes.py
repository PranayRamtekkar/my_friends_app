from app import app, db
from flask import jsonify, request
from models import Friend

@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result)

@app.route("/api/friends",methods=["POST"])
def add_friend():
    try:
        required_fields = ["name", "role", "description", "gender"]
        friend_data = request.json

        for field in required_fields:
            if field not in friend_data or not friend_data.get(field):
                return jsonify({"error":f"Missing required field {field}"}), 400

        name = friend_data.get("name")
        role = friend_data.get("role")
        description = friend_data.get("description")
        gender = friend_data.get("gender")

        #Fetch avatar image based on the gender
        if gender == "male".lower():
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female".lower():
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()
        return jsonify(new_friend.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/friends/<int:id>", methods=["PATCH"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404

        friend_data = request.json
        friend.name = friend_data.get("name", friend.name)
        friend.role = friend_data.get("role", friend.role)
        friend.description = friend_data.get("description", friend.description)
        friend.gender = friend_data.get("gender", friend.gender)

        db.session.commit()
        return jsonify(friend.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404

        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500