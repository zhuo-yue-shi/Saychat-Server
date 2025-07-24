from flask import Flask, jsonify, request
from waitress import serve
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, get_jwt)
from flask_cors import CORS

import datetime
import hashlib
import uuid
import json
import os
import logging

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'  # 实际生产环境中应使用安全的随机密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)

jwt = JWTManager(app)

# 数据文件路径
DATA_FILE = 'UsersData.json'

# 模拟数据库存储用户信息
users = {}
# 存储已撤销的令牌
revoked_tokens = set()
# 新注册的用户
register_users = []

# b
# y
# N
# Y
# Z
# Y

# 加载用户数据
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            # 转换数组格式为字典并映射字段名
            users = {}
            for user in users_data:
                username = user['Login_usersname']
                users[username] = {
                    'Usersname': user['Usersname'],
                    'Type': user['Type'],
                    'Password': user['Password'],
                    'Login_usersname': user['Login_usersname'],
                    'En_usersname': user['En_usersname'],
                    'id': str(uuid.uuid4()),
                    'created_at': datetime.datetime.utcnow().isoformat()
                }
    except Exception as e:
        logging.error(f"Error loading user data: {e}")
        users = {}
    else:
        logging.info(f"User data loaded successfully. Total users: {len(users)}")

# 保存用户数据
def save_user_data():
    # 本函数弃用
    pass

    # Convert users dictionary back to array format for saving
    # users_array = list(users.values())
    # Remove added fields not in original format
    # for user in users_array:
    #     user.pop('id', None)
    #     user.pop('created_at', None)
    # with open(DATA_FILE, 'w', encoding='utf-8') as f:
    #     json.dump(users_array, f, ensure_ascii=False, indent=2)

# 密码哈希函数
def hash_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'OK',
        'message': 'Server is running successfully'
    }), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_type = 3
    english_username = data.get('english_username')
    login_usersname = data.get('login_username')
    is_banned = False
    unban_time = 0

    logging.info(f"Registration attempt for username: {username}")

    # Validate required fields and type range
    if not username or not password or not email or user_type is None or not login_usersname or not english_username:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    if not isinstance(user_type, int) or not (1 <= user_type <= 6):
        return jsonify({'status': 'error', 'message': 'Type must be an integer between 1 and 6'}), 400

    if hash_password(login_usersname) in users:
        logging.warning(f"Registration failed - username already exists: {username}")
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    # 创建新用户
    users[hash_password(login_usersname)] = {
        'Usersname': username,
        'Type': str(user_type),
        'Password': hash_password(password),
        'Login_usersname': hash_password(login_usersname),
        'En_usersname': english_username,
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    register_users.append({
        'Usersname': username,
        'Type': str(user_type),
        'Password': hash_password(password),
        'Login_usersname': hash_password(login_usersname),
        'En_usersname': english_username,
        'created_at': datetime.datetime.utcnow().isoformat()
    })
    save_user_data()
    logging.info(f"User registered successfully: {username}")

    return jsonify({
        'status': 'success',
        'message': 'User registered successfully'
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    logging.info(f"Login attempt for username: {username}")

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing username or password'}), 400

    user = users.get(hash_password(username))
    logging.info(f"{user['Password']} | {hash_password(password)}")
    if not user or user['Password'] != hash_password(password):
        logging.warning(f"Login failed - invalid credentials for username: {username}")
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

    # 创建访问令牌和刷新令牌
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        'status': 'success',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = users.get(hash_password(current_user))
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # 返回用户信息
    ret = {
        'status': 'success',
        'data': {
            'Usersname': user['Usersname'],
            'Type': user['Type'],
            'Password': user['Password'],
            'Login_usersname': user['Login_usersname'],
            'En_usersname': user['En_usersname'],
            'created_at': user['created_at']
        }
    }
    return jsonify(ret), 200

@app.route('/user', methods=['PUT'])
@jwt_required()
def update_user_info():
    current_user = get_jwt_identity()
    user = users.get(current_user)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    data = request.get_json()
    logging.info(f"Update attempt for user: {current_user}")
    
    # 禁止修改特定字段
    disallowed_fields = ['Usersname', 'Unblock time', 'Type', 'Login_usersname', 'En_usersname', 'Banned', 'created_at']
    for field in disallowed_fields:
        if field in data:
            return jsonify({'status': 'error', 'message': f'{field}字段不允许通过API修改'}), 400
        
    if 'Password' in data:
        user['Password'] = hash_password(data['Password'])
    save_user_data()
    logging.info(f"User information updated: {current_user}")

    return jsonify({
        'status': 'success',
        'message': 'User information updated successfully'
    }), 200

@app.route('/token/verify', methods=['POST'])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()
    logging.info(f"Token verified for user: {current_user}")
    return jsonify({
        'status': 'success',
        'message': 'Token is valid',
        'exp': get_jwt()['exp']
    }), 200

@app.route('/user/checkRegisterUsers', methods=['GET'])
@jwt_required()
def check_register_users():
    current_user = get_jwt_identity()
    user = users.get(hash_password(current_user))
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    if not (user['Type'] == '1' or user['Type'] == '5'):
        return jsonify({'status': 'error', 'message': 'You are not an admin'}), 403

    return jsonify({
        'status': 'success',
        'data': register_users
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Server started on port {port}")
    serve(app, host='0.0.0.0', port=port)