# Saychat Server API Documentation

## Base URL
`http://localhost:5000`

## Authentication
Most endpoints require: `Authorization: Bearer <access_token>`

## Endpoints

### 1. Health Check
- **Path**: `/ping`
- **Method**: GET
- **Auth**: Not required
- **Response**:
  ```json
  {"status": "OK", "message": "Server is running successfully"}
  ```
- **Status Codes**: 200

### 2. User Registration
- **Path**: `/register`
- **Method**: POST
- **Auth**: Not required
- **Request Body**:
  ```json
  {"username": "string", "password": "string", "email": "string", "login_username": "string", "english_username": "string"}
  ```
- **Success Response**:
  ```json
  {"status": "success", "message": "User registered successfully", }
  ```
- **Error Response**:
  ```json
  {"status": "error", "message": "Missing required fields" | "Username already exists"}
  ```
- **Validation Rules**: type must be an integer between 1 and 6
- **Status Codes**: 201, 400

### 3. User Login
- **Path**: `/login`
- **Method**: POST
- **Auth**: Not required
- **Request Body**:
  ```json
  {"username": "string", "password": "string"}
  ```
- **Success Response**:
  ```json
  {"status": "success", "access_token": "string", "refresh_token": "string", "token_type": "bearer"}
  ```
- **Error Response**:
  ```json
  {"status": "error", "message": "Missing username or password" | "Invalid credentials"}
  ```
- **Status Codes**: 200, 400, 401

### 4. Refresh Access Token
- **Path**: `/refresh`
- **Method**: POST
- **Auth**: Required (refresh token)
- **Success Response**:
  ```json
  {"access_token": "string"}
  ```
- **Status Codes**: 200, 401

### 5. Get User Information
- **Path**: `/user`
- **Method**: GET
- **Auth**: Required
- **Success Response**:
  ```json
  {"status": "success", "data": {"Usersname": "string", "Type": "string", "Login_usersname": "string", "En_usersname": "string"}}
  ```
- **Error Response**:
  ```json
  {"status": "error", "message": "User not found"}
  ```
- **Status Codes**: 200, 401, 404

### 6. Update User Information
- **Path**: `/user`
- **Method**: PUT
- **Auth**: Required
- **Request Body**:
  ```json
  {"email": "string", "password": "string"} // Both optional
  ```
- **Success Response**:
  ```json
  {"status": "success", "message": "User information updated successfully"}
  ```
- **Status Codes**: 200, 401, 404

### 7. Verify Token
- **Path**: `/token/verify`
- **Method**: POST
- **Auth**: Required
- **Success Response**:
  ```json
  {"status": "success", "message": "Token is valid", "exp": "number"}
  ```
- **Status Codes**: 200, 401

### 8. Check Register Users (Admin Only)
- **Path**: `/user/checkRegisterUsers`
- **Method**: GET
- **Auth**: Required (Admin only)
- **Description**: Get list of newly registered users (Admin only)
- **Success Response**:
  ```json
  {"status": "success", "data": [{"Usersname": "string", "Type": "string", "Password": "string", "Login_usersname": "string", "En_usersname": "string"}]}
  ```
- **Error Response**:
  ```json
  {"status": "error", "message": "User not found" | "You are not an admin"}
  ```
- **Status Codes**: 200, 401, 403, 404