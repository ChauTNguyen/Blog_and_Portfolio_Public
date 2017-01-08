from app import db


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    email = db.Column(db.String(30), index=True, unique=True)

    def __init__(self, email):
        self.email = email

    def __str__(self):
        return '{' + str(self.id) + ': ' + self.email + '}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    blog_post_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(20), index=True)
    message = db.Column(db.String(360))

    # This is implemented in a really shitty way, but it's minor so no need to redesign it lol.
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    year = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    mark = db.Column(db.String(2)) # PM vs AM

    def __init__(self, blog_post_id, name, message, month, day, year, hour, minutes):
        self.blog_post_id = blog_post_id
        self.name = name
        self.message = message
        self.month = month
        self.day = day
        self.year = year

        if hour > 12:
            self.hour = hour - 12
            self.mark = 'PM'
        elif hour == 12:
            self.hour = 12
            self.mark = 'PM'
        else:
            if hour == 0:
                self.hour = 12
            else:
                self.hour = hour
            self.mark = 'AM'

        self.minutes = minutes

    def __str__(self):
        return '{' + self.name + ': ' + self.message + '}'