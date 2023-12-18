"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        '''Does the repr method work as expected?'''
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(repr(u), f"<User #{u.id}: testuser, test@test.com>")

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""
        user1 = User(
            email="user1@test.com",
            username="user1",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1)

        user2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user2)
        db.session.commit()

        user1.following.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))
        self.assertFalse(user2.is_following(user1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""
        user1 = User(
            email="user1@test.com",
            username="user1",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1)

        user2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user2)
        db.session.commit()

        user1.followers.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_followed_by(user2))
        self.assertFalse(user2.is_followed_by(user1))

    def test_signup(self):
        '''Does User.create successfully create a new user given valid credentials'''
        user1 = User.signup(
            username='username1',
            email='email1@gmail.com',
            password='hashed_pwd',
            image_url='www.image_url.com/png',
        )
        db.session.commit()

        self.assertIsInstance(user1, User)
        self.assertIsNotNone(User.query.filter_by(username='username1').first())
        self.assertTrue(user1.password, 'hashed_pwd')

        user2 = User.signup(
            username='username2',
            email='',
            password='hashed_pwd',
            image_url='www.image_url.com/png',
        )
        db.session.commit()
        
        self.assertNotIsInstance(user2, User)

    def test_authenticate(self):
        '''Does User.authenticate successfully return a user when given a valid username and password?'''
        user1 = User.signup(
            email="test@test.com",
            username="user1",
            password="HASHED_PASSWORD",
            image_url='www.image_url.com/png',
        )

        db.session.commit()

        authenticated_user = User.authenticate(username='user1', password='HASHED_PASSWORD')

        self.assertIsInstance(user1, User)
        self.assertEqual(authenticated_user.username, 'user1')

        wrong_password_user=User.authenticate(username='user1', password='wrong_password')

        self.assertFalse(wrong_password_user)

