#!env/bin/python
import datetime
import os
import unittest

import flask

from app import app, db, models
from app.config import basedir


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_comment(self):
        a = datetime.datetime.now()
        d = datetime.datetime.now().time()

        c = models.Comment(1, "Chau", "Hey, my name is Chau.",
                           a.month, a.day, a.year,
                           d.hour, d.minute)

        number_of_comments = len(models.Comment.query.all())

        # The comment's ID should always be number_of_comments plus 1.
        next_id = number_of_comments + 1

        db.session.add(c)
        db.session.commit()

        number_of_comments += 1

        assert len(models.Comment.query.all()) == number_of_comments
        assert c.id == next_id
        assert c.blog_post_id == 1
        assert c.name == "Chau"
        assert c.message == "Hey, my name is Chau."

    def test_subscribe_user(self):
        s = models.Subscriber("the.chau.96@gmail.com")

        number_of_subscribers = len(models.Subscriber.query.all())
        assert number_of_subscribers == 0

        # The subscriber's ID should always be number_of_subscribers plus 1.
        next_id = number_of_subscribers + 1

        db.session.add(s)
        db.session.commit()

        number_of_subscribers += 1

        assert len(models.Subscriber.query.all()) == number_of_subscribers
        assert len(models.Subscriber.query.all()) != 0
        assert len(models.Subscriber.query.all()) == 1
        assert s.email == "the.chau.96@gmail.com"
        assert s.id == 1
        assert s.id == next_id

    def test_subscribe_and_unsubscribe(self):
        assert len(models.Subscriber.query.all()) == 0

        # Add a user.
        s = models.Subscriber("the.chau.96@gmail.com")
        db.session.add(s)
        db.session.commit()

        number_of_subscribers = len(models.Subscriber.query.all())
        assert number_of_subscribers == 1

        # Delete the user.
        subscriber = models.Subscriber.query.get(number_of_subscribers)
        db.session.delete(subscriber)
        db.session.commit()
        assert number_of_subscribers - 1 == len(models.Subscriber.query.all()) # 0 == 0

    def test_index_page(self):
        app = flask.Flask(__name__)
        with app.test_request_context('/'):
            assert flask.request.path == '/'
            assert flask.request.method == 'GET'
        with app.test_request_context('/index'):
            assert flask.request.path == '/index'
            assert flask.request.method == 'GET'

    def test_blog_home_page(self):
        app = flask.Flask(__name__)
        with app.test_request_context('/blog/0'):
            assert flask.request.path == '/blog/0'
            assert flask.request.method == 'GET'

    def test_blog_page_1(self):
        app = flask.Flask(__name__)
        with app.test_request_context('/blog/1'):
            assert flask.request.path == '/blog/1'
            assert flask.request.path[-1:] == str(1)
            assert flask.request.method == 'GET'

    def test_blog_page_2(self):
        app = flask.Flask(__name__)
        with app.test_request_context('/blog/2'):
            assert flask.request.path == '/blog/2'
            assert flask.request.path[-1:] == str(2)
            assert flask.request.method == 'GET'

    def test_blog_page_3(self):
        app = flask.Flask(__name__)
        with app.test_request_context('/blog/3'):
            assert flask.request.path == '/blog/3'
            assert flask.request.path[-1:] == str(3)
            assert flask.request.method == 'GET'
            # assert flask.request.args.get('post_id') == 3
            # assert flask.request.args['post_id'] == 3

    def test_empty_db(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'' in response.data

    def test_add_comment_to_blog_page_1(self):
        a = datetime.datetime.now()
        d = datetime.datetime.now().time()

        c = models.Comment(1, "Chau", "Hey, my name is Chau.",
                           a.month, a.day, a.year,
                           d.hour, d.minute)

        db.session.add(c)
        assert c in db.session
        db.session.commit()

        comments = db.session.query(models.Comment).filter(models.Comment.blog_post_id == 1)

        assert comments[0] == c
        assert comments[0].id == 1
        assert comments[0].blog_post_id == 1
        assert comments[0].name == "Chau"
        assert comments[0].message == "Hey, my name is Chau."
        assert comments.count() == 1

    def test_add_comment_to_blog_page_2(self):
        a = datetime.datetime.now()
        d = datetime.datetime.now().time()

        c = models.Comment(2, "Bob", "Hey, my name is Bob.",
                           a.month, a.day, a.year,
                           d.hour, d.minute)

        db.session.add(c)
        assert c in db.session
        db.session.commit()

        comments = db.session.query(models.Comment).filter(models.Comment.blog_post_id == 2)

        assert comments[0] == c
        assert comments[0].id == 1
        assert comments[0].blog_post_id == 2
        assert comments[0].name == "Bob"
        assert comments[0].message == "Hey, my name is Bob."
        assert comments.count() == 1

    def test_add_comment_to_blog_page_3(self):
        a = datetime.datetime.now()
        d = datetime.datetime.now().time()

        c = models.Comment(3, "Chau", "Hey, my name is Chau.",
                           a.month, a.day, a.year,
                           d.hour, d.minute)

        db.session.add(c)
        assert c in db.session
        db.session.commit()

        comments = db.session.query(models.Comment).filter(models.Comment.blog_post_id == 3)

        assert comments[0] == c
        assert comments[0].id == 1
        assert comments[0].blog_post_id == 3
        assert comments[0].name == "Chau"
        assert comments[0].message == "Hey, my name is Chau."
        assert comments.count() == 1

    def test_add_3_comments_to_blog_page_1(self):
        a = datetime.datetime.now()
        d = datetime.datetime.now().time()

        c1 = models.Comment(1, "Chau", "Hey, my name is Chau.",
                           a.month, a.day, a.year,
                           d.hour, d.minute)

        c2 = models.Comment(1, "Ray", "Hey, my name is Ray.",
                            a.month, a.day, a.year,
                            d.hour, d.minute)

        c3 = models.Comment(1, "Bob", "Hey, my name is Bob.",
                            a.month, a.day, a.year,
                            d.hour, d.minute)

        comments_to_add = [c1, c2, c3]

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)

        for c in comments_to_add:
            assert c in db.session

        db.session.commit()

        comments = db.session.query(models.Comment).filter(models.Comment.blog_post_id == 1)

        assert comments[0] == c1
        assert comments[1] == c2
        assert comments[2] == c3
        assert comments[0].id == 1
        assert comments[1].id == 2
        assert comments[2].id == 3
        for i in range(0, 3):
            assert comments[i].blog_post_id == 1
        assert comments[0].name == "Chau"
        assert comments[1].name == "Ray"
        assert comments[2].name == "Bob"
        assert comments[0].message == "Hey, my name is Chau."
        assert comments[1].message == "Hey, my name is Ray."
        assert comments[2].message == "Hey, my name is Bob."
        assert comments.count() == 3

    # Add tests for UX, use some html scraping thingy.

if __name__ == '__main__':
    unittest.main()