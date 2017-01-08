# Basic security
WTF_CSRF_ENABLED = True
SECRET_KEY = ''

# Email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# Administrator list for contact form
ADMINS = ['ChauTNguyen96@gmail.com']

# Set up database.
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import psycopg2

RUN_LOCAL = True

if not RUN_LOCAL:
    try:
        import urlparse as urlparse
    except:
        pass
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    if os.environ.get('SQLALCHEMY_DATABASE_URI') is None:
        SQLALCHEMY_DATABASE_URI = ""
else:
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/blog"