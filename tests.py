"""Test suite for Fetch app."""

from model import connect_to_db
from server import app
import unittest


class FlaskTests(unittest.TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to fake database
        connect_to_db(app)

    def test_index(self):
        """Does the index redirect to homepage?"""

        result = self.client.get('/')

        self.assertEqual(result.status_code, 302)
        self.assertIn('text/html', result.headers['Content-Type'])

    def test_homepage(self):
        """Does the homepage load correctly?"""

        result = self.client.get('/home')

        self.assertEqual(result.status_code, 200)
        self.assertIn('text/html', result.headers['Content-Type'])
        self.assertIn('FETCH', result.data)

###############################################################################

if __name__ == "__main__":
    unittest.main()
