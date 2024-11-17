from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Swagger UI configuration
SWAGGER_URL = "/api-docs"
API_URL = "/helloswag.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve the OpenAPI YAML file
@app.route("/helloswag.yaml")
def serve_swagger_yaml():
    return send_from_directory(".", "helloswag.yaml")


users = {
    1: {"name": "Superman", "email": "superman@example.com"},
    2: {"name": "Batman", "email": "batman@example.com"}
}


@app.route("/users", methods=["GET"])
def get_all_users():
    """Get all users"""
    return jsonify({"users": users}), 200

@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    user_id_counter = len(users)+1
    data = request.get_json()
    user = {"id": user_id_counter, "name": data.get("name"), "email": data.get("email")}
    users[user_id_counter] = user
    user_id_counter += 1
    return jsonify(user), 201

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """Get a user by ID"""
    user = users.get(id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    """Update a user by ID"""
    data = request.get_json()
    user = users.get(id)
    if user:
        user["name"] = data.get("name", user["name"])
        user["email"] = data.get("email", user["email"])
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    """Delete a user by ID"""
    user = users.pop(id, None)
    if user:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
