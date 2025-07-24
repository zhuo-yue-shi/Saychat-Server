import requests
import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000"
        
    def test_ping_endpoint(self):
        """Test the /ping endpoint"""
        response = requests.get(f"{self.base_url}/ping")
        
        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check response format
        self.assertEqual(response.headers["Content-Type"], "application/json")
        
        # Check response content
        response_data = response.json()
        self.assertEqual(response_data.get("status"), "OK")
        self.assertEqual(response_data.get("message"), "Server is running successfully")

    def test_user_registration(self):
        """Test user registration functionality"""
        # Test with valid data
        user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com"
        }
        response = requests.post(f"{self.base_url}/register", json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("status"), "success")
        self.assertIsNotNone(response.json().get("user_id"))

        # Test with duplicate username
        response = requests.post(f"{self.base_url}/register", json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("status"), "error")

        # Test with missing fields
        response = requests.post(f"{self.base_url}/register", json={"username": "incompleteuser"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("status"), "error")

    def test_user_login(self):
        """Test user login functionality"""
        # First register a test user
        user_data = {
            "username": "loginuser",
            "password": "loginpassword",
            "email": "login@example.com"
        }
        requests.post(f"{self.base_url}/register", json=user_data)

        # Test with valid credentials
        login_data = {
            "username": "loginuser",
            "password": "loginpassword"
        }
        response = requests.post(f"{self.base_url}/login", json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")
        self.assertIsNotNone(response.json().get("access_token"))
        self.assertIsNotNone(response.json().get("refresh_token"))

        # Test with invalid credentials
        invalid_login = {
            "username": "loginuser",
            "password": "wrongpassword"
        }
        response = requests.post(f"{self.base_url}/login", json=invalid_login)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get("status"), "error")

    def test_token_functionality(self):
        """Test token generation, refresh, and verification"""
        # Register and login to get tokens
        user_data = {
            "username": "tokenuser",
            "password": "tokenpassword",
            "email": "token@example.com"
        }
        requests.post(f"{self.base_url}/register", json=user_data)

        login_response = requests.post(f"{self.base_url}/login", json={
            "username": "tokenuser",
            "password": "tokenpassword"
        })
        tokens = login_response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        # Test token verification
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{self.base_url}/token/verify", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")

        # Test token refresh
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = requests.post(f"{self.base_url}/refresh", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get("access_token"))

    def test_protected_endpoints(self):
        """Test access to protected endpoints"""
        # Register and login to get tokens
        user_data = {
            "username": "protecteduser",
            "password": "protectedpassword",
            "email": "protected@example.com"
        }
        requests.post(f"{self.base_url}/register", json=user_data)

        login_response = requests.post(f"{self.base_url}/login", json={
            "username": "protecteduser",
            "password": "protectedpassword"
        })
        access_token = login_response.json().get("access_token")

        # Test accessing protected endpoint with valid token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.base_url}/user", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")
        self.assertEqual(response.json().get("data").get("username"), "protecteduser")

        # Test accessing protected endpoint without token
        response = requests.get(f"{self.base_url}/user")
        self.assertEqual(response.status_code, 401)

        # Test updating user information
        update_data = {"email": "updated@example.com"}
        response = requests.put(f"{self.base_url}/user", json=update_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "success")

        # Verify the information was updated
        response = requests.get(f"{self.base_url}/user", headers=headers)
        self.assertEqual(response.json().get("data").get("email"), "updated@example.com")

if __name__ == "__main__":
    unittest.main()