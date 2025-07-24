# API文档 (中文)

## 基础信息
- 基础URL: `/`
- 所有请求和响应均使用JSON格式
- 需要认证的接口需在请求头中包含: `Authorization: Bearer {access_token}`

## 公共接口

### 健康检查
- **URL**: `/ping`
- **方法**: GET
- **描述**: 检查服务器是否正常运行
- **响应**: 
  ```json
  {
    "status": "OK",
    "message": "Server is running successfully"
  }
  ```

### 用户注册
- **URL**: `/register`
- **方法**: POST
- **描述**: 创建新用户账号
- **请求体**: 
  ```json
  {
    "username": "用户名",
    "password": "密码",
    "email": "邮箱地址",
    "type": 1-6之间的整数,
    "english_username": "英文用户名(可选)",

  }
  ```
- **响应**: 
  ```json
  {
    "status": "success",
    "message": "User registered successfully",
    "user_id": "用户ID"
  }
  ```

### 用户登录
- **URL**: `/login`
- **方法**: POST
- **描述**: 用户登录并获取访问令牌
- **请求体**: 
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- **响应**: 
  ```json
  {
    "status": "success",
    "access_token": "访问令牌",
    "refresh_token": "刷新令牌",
    "token_type": "bearer"
  }
  ```

### 刷新访问令牌
- **URL**: `/refresh`
- **方法**: POST
- **描述**: 使用刷新令牌获取新的访问令牌
- **请求头**: 需要包含刷新令牌
- **响应**: 
  ```json
  {
    "access_token": "新的访问令牌"
  }
  ```

### 验证令牌
- **URL**: `/token/verify`
- **方法**: POST
- **描述**: 验证访问令牌是否有效
- **请求头**: 需要包含访问令牌
- **响应**: 
  ```json
  {
    "status": "success",
    "message": "Token is valid",
    "exp": 令牌过期时间戳
  }
  ```

## 需要认证的接口

### 获取用户信息
- **URL**: `/user`
- **方法**: GET
- **描述**: 获取当前登录用户的信息
- **请求头**: 需要包含访问令牌
- **响应**: 
  ```json
  {
    "status": "success",
    "data": {
      "id": "用户ID",
      "username": "用户名",
      "email": "邮箱地址",
      "type": 用户类型,
      "english_username": "英文用户名",
      "is_banned": 是否被封禁,
      "unban_time": 解封时间,
      "created_at": "创建时间"
    }
  }
  ```

### 更新用户信息
- **URL**: `/user`
- **方法**: PUT
- **描述**: 更新当前登录用户的信息
- **请求头**: 需要包含访问令牌
- **请求体**: 
  ```json
  {
    "email": "新邮箱地址(可选)",
    "password": "新密码(可选)"
  }
  ```
- **响应**: 
  ```json
  {
    "status": "success",
    "message": "User information updated successfully"
  }
  ```