from app import db, models

comments = models.Comment.query.all()
for comment in comments:
    db.session.delete(comment)
db.session.commit()