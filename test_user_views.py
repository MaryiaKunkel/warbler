"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_users_show(self):
        """When you’re logged in, can you see the follower / following pages for any user?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            # can now make requests to flask via `client`
            user2=User(username="testuser2",
                        email="test2@test.com",
                        password="testuser",
                        image_url=None)
            
            user2.followers.append(self.testuser)
            user2.following.append(self.testuser)
            db.session.add(user2)
            db.session.commit()

            resp = c.get(f'/users/{user2.id}', follow_redirects=True)
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200)
        

            self.assertIn(f'<p class="small">Followers</p><h4><a href="/users/{user2.id}/followers">1</a></h4>'.replace('\n', '').replace(' ', ''), html.replace(' ', '').replace('\n', ''))

            self.assertIn(f'<p class="small">Following</p><h4><a href="/users/{user2.id}/following">1</a></h4>'.replace('\n', '').replace(' ', ''), html.replace(' ', '').replace('\n', ''))
            
    def test_users_show_when_logged_out(self):
        """When you're logged out, can you see the follower / following pages for any user?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            # can now make requests to flask via `client`
            c.get('/logout', follow_redirects=True)

            user2=User(username="testuser2",
                        email="test2@test.com",
                        password="testuser",
                        image_url=None)
                        
            db.session.add(user2)
            db.session.commit()

            resp = c.get(f'/users/{user2.id}')

            self.assertEqual(resp.status_code, 200)

    def test_add_message(self):
        '''When you're logged in, can you add a message as yourself?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)


            html = resp.get_data(as_text=True) 
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello', html)

    def test_delete_message(self):
        '''When you're logged in, can you delete a message as yourself?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            message=Message(
                text='test',
                user_id=self.testuser.id
            )

            db.session.add(message)
            db.session.commit()
            resp = c.post(f'/messages/{message.id}/delete')

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.first()
            self.assertIsNone(msg)

    def test_add_message_when_logged_out(self):
        '''When you're logged out, are you prohibited from adding messages?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                c.get('/logout', follow_redirects=True)

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)


            html = resp.get_data(as_text=True) 
            print(html)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Log in', html)

    def test_delete_message_when_logged_out(self):
        '''When you're logged out, are you prohibited from deleting messages?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                c.get('/logout', follow_redirects=True)

            message=Message(
                text='test',
                user_id=self.testuser.id
            )

            db.session.add(message)
            db.session.commit()
            resp = c.post(f'/messages/{message.id}/delete', follow_redirects=True)

            html = resp.get_data(as_text=True) 
            print(html)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Log in', html)

    def test_add_message_as_another_user_when_logged_in(self):
        '''When you're logged in, are you prohibiting from adding a message as another user?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            user2=User.signup(username="testuser2",
                       email="test2@test.com",
                       password="testuser",
                       image_url=None)
            db.session.commit()
            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            # html=resp.get_data(as_text=True)
            # print(html)
            self.assertEqual(resp.status_code, 403)



    def test_delete_message_as_another_user_when_logged_in(self):      
        '''When you're logged in, are you prohibiting from deleting a message as another user?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            user2=User.signup(username="testuser2",
                       email="test2@test.com",
                       password="testuser",
                       image_url=None)
            
            db.session.commit()

            message=Message(
                text='test',
                user_id=self.testuser.id
            )

            db.session.add(message)
            db.session.commit()

            resp = c.post(f'/messages/{message.id}/delete', follow_redirects=True)

            # html = resp.get_data(as_text=True) 
            # print(html)
            self.assertEqual(resp.status_code, 403)


