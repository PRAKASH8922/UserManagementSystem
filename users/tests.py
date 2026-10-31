import json
from django.test import TestCase, Client
from django.contrib.auth.hashers import check_password, make_password
from users.models import CtUserDetails
from users.user import User


class UserManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CtUserDetails.objects.create(
            name='Test User',
            phone='9876543210',
            email='test@example.com',
            password=make_password('TestPass@123')
        )

    def test_page_renders(self):
        """Test that index, login, and signup pages render with status 200."""
        for path in ['/', '/index.html', '/login', '/login.html', '/signup', '/signup.html']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, f"Path {path} failed to load.")

    def test_get_users_list(self):
        """Test GET /user returns user list and never exposes password."""
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test User')
        self.assertEqual(data[0]['email'], 'test@example.com')
        self.assertNotIn('password', data[0])

    def test_create_user(self):
        """Test POST /user hashes password and returns 201 without password."""
        payload = {
            'name': 'Jane Doe',
            'phone': '1234567890',
            'email': 'jane@example.com',
            'password': 'SecurePassword@123'
        }
        response = self.client.post(
            '/user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['name'], 'Jane Doe')
        self.assertEqual(data['email'], 'jane@example.com')
        self.assertNotIn('password', data)

        created_user = CtUserDetails.objects.get(email='jane@example.com')
        self.assertTrue(check_password('SecurePassword@123', created_user.password))

    def test_create_user_duplicate_email(self):
        """Test POST /user rejects duplicate email."""
        payload = {
            'name': 'Duplicate User',
            'phone': '1234567890',
            'email': 'test@example.com',
            'password': 'Password@123'
        }
        response = self.client.post(
            '/user',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        """Test PUT /user/<id> updates user and hashes updated password."""
        payload = {
            'name': 'Updated Name',
            'phone': '9998887776',
            'email': 'updated@example.com',
            'password': 'NewPassword@123'
        }
        response = self.client.put(
            f'/user/{self.user.id}',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Updated Name')
        self.assertNotIn('password', data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.phone, '9998887776')
        self.assertTrue(check_password('NewPassword@123', self.user.password))

    def test_delete_user(self):
        """Test DELETE /user/<id> removes user and returns 204."""
        response = self.client.delete(f'/user/{self.user.id}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CtUserDetails.objects.filter(id=self.user.id).exists())

    def test_user_login_success(self):
        """Test POST /user/login returns matched user details for valid credentials."""
        payload = {
            'email': 'test@example.com',
            'password': 'TestPass@123'
        }
        response = self.client.post(
            '/user/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], 'test@example.com')
        self.assertEqual(data[0]['name'], 'Test User')
        self.assertNotIn('password', data[0])

    def test_user_login_failure(self):
        """Test POST /user/login returns [] for invalid credentials."""
        payload = {
            'email': 'test@example.com',
            'password': 'WrongPassword@123'
        }
        response = self.client.post(
            '/user/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [])

    def test_user_class_helper(self):
        """Test User class helper parity with User.js."""
        u = User(1, 'Alice', 'alice@example.com')
        self.assertEqual(u.get_user_details(), "ID: 1, Name: Alice, Email: alice@example.com")
