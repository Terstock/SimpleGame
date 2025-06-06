from models import db, Game
from app import app

with app.app_context():
    game_to_delete = Game.query.get(186) 
    if game_to_delete:
        db.session.delete(game_to_delete)
        db.session.commit()
        print("Видалено гру:", game_to_delete.title)
    else:
        print("Гру не знайдено.")