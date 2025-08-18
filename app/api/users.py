# app/api/users.py
from flask import Blueprint, request, jsonify
from app.models import db, User

# 创建一个名为 'users_api' 的蓝图
users_api_bp = Blueprint('users_api', __name__)

@users_api_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@users_api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@users_api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({"error": "Missing username or email"}), 400
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# ... (PUT 和 DELETE 的代码也一样复制过来，但要把 @app.route 改成 @users_api_bp.route) ...

@users_api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@users_api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


# app/api/users.py
# ... (在文件末尾追加) ...

@users_api_bp.route('/test-500', methods=['GET'])
def test_500_error():
    # 我们在这里故意制造一个无法处理的bug
    # 任何数除以0都会在Python中引发 ZeroDivisionError
    result = 1 / 0
    return jsonify({"message": "You will never see this message"})