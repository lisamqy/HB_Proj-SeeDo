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
            self.assertIn(b"New User?", result.data)
        elif session:
            self.assertIn(b"View your account details", result.data)

    def test_login_success(self):
        result = self.client.post("/",
                                    data={'Email': "user1@email.com", 'Password': "123"},
                                    follow_redirects=True)
        self.assertNotIn(b"New User?", result.data)
        self.assertIn(b"Welcome", result.data)
    
    def test_registration_success(self):
        result = self.client.post("/new",
                                    data={'Username': "user99", 'Email': "user99@email.com", 'Password': "123"},
                                    follow_redirects=True)
        self.assertNotIn(b"Register Here!", result.data)




if __name__ == "__main__":
    unittest.main()
