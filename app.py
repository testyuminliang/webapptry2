from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- 模拟数据库 ---
# 用一个列表来存储所有用户数据
users_db = [
    {
        "id": 101,
        "username": "SuperCoder",
        "skills": ["Python", "Flask", "API Design"]
    },
    {
        "id": 102,
        "username": "DataQueen",
        "skills": ["SQL", "Pandas", "ETL"]
    }
]
# 用于创建新用户时分配ID
# 在真实应用中，这会由数据库自动处理
next_user_id = 103

# --- GET (查询所有用户) ---
@app.route('/api/users', methods=['GET'])
def get_all_users():
    # ## 新增功能 ##: 检查URL中是否有'fields'查询参数
    fields_to_show = request.args.getlist('fields')

    # 如果没有'fields'参数，就返回完整的用户列表
    if not fields_to_show:
        return jsonify(users_db)
    
    # 如果有'fields'参数，就为列表中的每个用户筛选字段
    filtered_users = []
    for user in users_db:
        filtered_user_data = {}
        for field in fields_to_show:
            if field in user:
                filtered_user_data[field] = user[field]
        filtered_users.append(filtered_user_data)
        
    return jsonify(filtered_users)

# --- GET (查询单个用户) ---
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    # 使用 next() 来查找用户，如果找不到则返回 None
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    # 如果找不到用户，返回 404 Not Found 错误
    return jsonify({"error": "User not found！！"}), 404

# --- POST (创建新用户) ---
@app.route('/api/users', methods=['POST'])
def create_user():
    global next_user_id
    # ## 修正 ##: 检查请求体中是否有合法的JSON数据
    new_user_data = request.get_json()
    if not new_user_data:
        return jsonify({"error": "Invalid input: No JSON body provided"}), 400
    
    if 'username' not in new_user_data:
        return jsonify({"error": "Invalid input: Missing username"}), 400
    
    new_user = {
        "id": next_user_id,
        "username": new_user_data['username'],
        "skills": new_user_data.get('skills', []) # 使用 .get() 提供默认值，更安全
    }
    users_db.append(new_user)
    next_user_id += 1
    # 返回 201 Created，表示资源创建成功
    return jsonify(new_user), 201

# --- PUT (更新用户) ---
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # ## 修正 ##: 同样检查请求体中是否有合法的JSON数据
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "Invalid input: No JSON body provided"}), 400
        
    # 使用字典的 update 方法，安全地更新用户信息
    user.update(update_data)
    return jsonify(user)

# --- DELETE (删除用户) ---
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_to_delete = next((user for user in users_db if user["id"] == user_id), None)
    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404
    
    # ## 修正 ##: 使用 list.remove() 方法直接在列表中删除元素
    users_db.remove(user_to_delete)
    # 返回 204 No Content，表示成功处理，但没有内容返回
    return '', 204

# --- POST (创建新用户并上传简历，使用 form-data) ---
@app.route('/api/users/with-resume', methods=['POST'])
def create_user_with_resume():
    global next_user_id
    
    # ## 重点 ##: 对于 form-data, 我们用 request.form 来获取文本字段
    # 这和 request.get_json() 是不同的！
    username = request.form.get('username')
    skills_str = request.form.get('skills') # form-data里的所有值都是字符串

    # ## 重点 ##: 对于 form-data, 我们用 request.files 来获取文件
    resume_file = request.files.get('resume_file')

    # --- 数据校验 ---
    if not username:
        return jsonify({"error": "Missing username in form data"}), 400
    if not resume_file:
        return jsonify({"error": "Missing resume_file in form data"}), 400

    # --- 处理数据 ---
    new_user = {
        "id": next_user_id,
        "username": username,
        "skills": skills_str.split(',') if skills_str else [], # 简单处理一下技能字符串
        "resume_filename": resume_file.filename # 获取上传的文件名
    }
    
    # --- 保存文件 ---
    # !! 重要: 请确保您的项目根目录下有一个名为 'uploads' 的文件夹 !!
    try:
        resume_file.save(f'uploads/{resume_file.filename}')
    except FileNotFoundError:
        # 如果 'uploads' 文件夹不存在，这是一个很好的实践来返回一个清晰的错误
        return jsonify({"error": "Server configuration error: 'uploads' directory not found."}), 500

    users_db.append(new_user)
    next_user_id += 1
    
    return jsonify({
        "message": "User created successfully with resume.",
        "user_data": new_user
    }), 201

# --- POST (快速修改用户名，使用 x-www-form-urlencoded) ---
@app.route('/api/users/<int:user_id>/change-username', methods=['POST'])
def change_username(user_id):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # ## 重点 ##: 同样使用 request.form 来获取 urlencoded 的数据
    new_username = request.form.get('new_username')
    
    if not new_username:
        return jsonify({"error": "Missing 'new_username' field in form"}), 400
        
    user['username'] = new_username
    return jsonify({
        "message": "Username updated successfully",
        "user": user
    })

# --- POST (上传头像，使用 binary) ---
@app.route('/api/users/<int:user_id>/avatar', methods=['POST'])
def upload_avatar(user_id):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # ## 重点 ##: 使用 request.data 获取原始的二进制Body
    avatar_binary_data = request.data
    if not avatar_binary_data:
        return jsonify({"error": "No binary data in request body"}), 400

    # -- 保存文件 --
    # 从请求头获取文件类型来决定后缀名，这是一个好习惯
    content_type = request.headers.get('Content-Type', 'image/png')
    extension = content_type.split('/')[-1]
    filename = f'{user_id}_avatar.{extension}'
    
    try:
        with open(f'uploads/{filename}', 'wb') as f:
            f.write(avatar_binary_data)
    except FileNotFoundError:
        return jsonify({"error": "Server configuration error: 'uploads' directory not found."}), 500

    return jsonify({
        "message": f"Avatar for user {user_id} uploaded successfully as {filename}"
    })

# --- 首页路由 (保持不变) ---
@app.route('/')
def home_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)