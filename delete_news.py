from app import app
from models import db, News

with app.app_context():
    News.query.delete()
    db.session.commit()
    print("Всі новини видалено.")