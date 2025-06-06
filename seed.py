from app import app
from models import db, Game
from datetime import date

with app.app_context():
    new_game = Game(
        title="Elden Ring",
        description="Фентезі-екшн з відкритим світом від творців Dark Souls.",
        release_date=date(2022, 2, 25),
        developer="FromSoftware",
        genre="Action RPG",
        platform="PC, PS4, PS5, Xbox",
        cover_image="https://res.cloudinary.com/dwnxgjd7u/image/upload/v1749108993/elden_ring_whwbh0.jpg"  
    )
    db.session.add(new_game)
    db.session.commit()
    print("✅ Ігру додано в базу!")