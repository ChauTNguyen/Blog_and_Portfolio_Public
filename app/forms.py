from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators


class ContactForm(Form):
    name = StringField("Name",
                       [validators.DataRequired("Please enter your name."),
                        validators.Length(max=20)])
    email = StringField("Email",
                        [validators.DataRequired("Please enter your email address."),
                         validators.Email(),
                         validators.Length(max=30)])
    subject = StringField("Subject",
                          [validators.DataRequired("Please enter a subject."),
                           validators.Length(max=25)])
    message = TextAreaField("Message",
                            [validators.DataRequired("Please enter a message."),
                             validators.Length(max=360)])
    submit = SubmitField("Send")


class SubscribeForm(Form):
    email = StringField("",
                        [validators.DataRequired("Please enter your email address."),
                         validators.Email(),
                         validators.Length(max=30)],
                        render_kw={"placeholder": "Email Address"})
    submit = SubmitField("Subscribe")


class CommentForm(Form):
    nickname = StringField("Nickname",
                           [validators.DataRequired("Please enter your nickname."),
                            validators.Length(max=12)],
                           render_kw={"placeholder": "Nickname"})
    message = TextAreaField("Comment",
                            [validators.DataRequired("Please enter a comment."),
                             validators.Length(max=120)],
                            render_kw={"placeholder": "Enter your comment here."})
    submit = SubmitField("Post comment")