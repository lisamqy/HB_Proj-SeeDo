import unittest

from flask import session
from server import app
from model import connect_to_db

class ServerTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app)

    def test_homepage(self):
        result = self.client.get("/")
        if not session:
            self.assertNotIn(b"Logout", result.data)
        elif session:
            self.assertIn(b"View account", result.data)

    def test_login_success(self):
        result = self.client.post("/",
                                    data={'Email': "user1@email.com", 'Password': "123"},
                                    follow_redirects=True)
        self.assertNotIn(b"Sign Up", result.data)
    
    def test_registration_page(self):
        result = self.client.get("/new")
        self.assertIn(b"Register Here!", result.data)
        self.assertIn(b"username", result.data)

    def test_search_page(self):
        result = self.client.get("/search")
        self.assertIn(b"Event Search Results", result.data)

    def test_user_page(self):
        result = self.client.get("/user/10")
        self.assertNotIn(b"Sign Up", result.data)
        self.assertIn(b"Liked events", result.data)

    def test_logout(self):
        result = self.client.get("/goodbye",
                                    follow_redirects=True)
        self.assertNotIn(b"View Account", result.data)
        self.assertIn(b"Sign Up", result.data)



if __name__ == "__main__":
    unittest.main()
