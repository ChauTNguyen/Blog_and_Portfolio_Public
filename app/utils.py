import datetime
import tzlocal, pytz

from flask import flash
from flask_mail import Message

from app import app, db, mail, models
from .decorators import async


def get_blog_info():
    """
    Brief: This is what automates everything within my blog.

    Returns a json-like structure containing information about each blog post.
    This helps automate a lot of things within templates.
    I can simply add information about a post by adding another object
    to the list (with the number being incremented), create a file called
    '<post_id>.html'. The links will be created because of my template code (I pass
    in many variables from views.py to the templates) and that post will be available to the user.
    """
    return {
        'posts': [
            {
                '1': {
                    'post-id': 1,
                    'title': "Welcome",
                    'last_updated': 'April X, 2016',
                    'tags': ['intro']
                },
                '2': {
                    'post-id': 2,
                    'title': "Side-projects P1: Developing My First Side-Projects as a Beginner",
                    'last_updated': 'June 24, 2016',
                    'tags': ['college', 'habits', 'beginner', 'tech', 'series']
                },
                '3': {
                    'post-id': 3,
                    'title': "Side-projects P2: The White Screen of Death",
                    'last_updated': 'June 24, 2016',
                    'tags': ['tech', 'beginner', 'projects', 'series'],
                },
                '4': {
                    'post-id': 4,
                    'title': "Side-projects P3: The Joy of DIY",
                    'last_updated': 'June 24, 2016',
                    'tags':  ['tech', 'beginner', 'projects', 'series']
                },
                '5': {
                    'post-id': 5,
                    'title': "Passion Outside of Computer Science",
                    'last_updated': 'June 25, 2016',
                    'tags': ['beginner', 'passion', 'career', 'life']
                },
                '6': {
                    'post-id': 6,
                    'title': "Python is Great for a Beginner",
                    'last_updated': 'July 29, 2016',
                    'tags': ['beginner', 'programming', 'projects']
                }
            }
        ]
    }


@async
def post_comment(app, blog_post_id, nickname, message):
    """Add a comment to the table."""
    with app.app_context():
        datetime_obj = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))

        a = datetime_obj
        d = datetime_obj.time()

        c = models.Comment(blog_post_id=blog_post_id, name=nickname, message=message,
                           month=a.month, day=a.day, year=a.year,
                           hour=d.hour, minutes=d.minute)

        db.session.add(c)
        db.session.commit()


def send_contact_email(subject, sender, recipients, email, message):
    """Send an email from /contact directly to the ADMINS list."""
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    msg.body = """
    From: %s <%s>
    %s
    """ % (subject, email, message)
    send_async_email(app, msg)


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def subscribe(email):
    """Add an email to the Subscriber table."""
    query = db.session.query(models.Subscriber).filter(models.Subscriber.email == email).first()

    if query is None:
        e = models.Subscriber(email=email)
        db.session.add(e)
        db.session.commit()
        msg = Message("Thank you for subscribing.",
                      sender='ChauTNguyen96@gmail.com',
                      recipients=[email])
        # msg.body = "To unsubscribe, click here: \nhttp://127.0.0.1:5000/unsubscribe/" + str(e.id) + "/" + e.email
        msg.body = "To unsubscribe, click here: \nhttps://cnguyen.herokuapp.com/unsubscribe/" + str(e.id) + "/" + e.email
        send_async_email(app, msg)
    else:
        flash("That email is already subscribed.")


def reset_subscribers():
    """Clear the entire Subscriber table."""
    subscribers = models.Subscriber.query.all()
    for subscriber in subscribers:
        db.session.delete(subscriber)
    db.session.commit()


def reset_comments():
    """Clear the entire Comment table."""
    comments = models.Comment.query.all()
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()


def flash_all_errors_from_form(form):
    """Flash every single error given by a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)


def get_comments_for_blog_post(post_id):
    """Returns a list of comments for a specific blog post."""
    return db.session.query(models.Comment)\
        .filter(models.Comment.blog_post_id == post_id)\
        .order_by(models.Comment.id.desc())