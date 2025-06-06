from flask import Flask, render_template, request
from models import db, Game, News
import os

app = Flask(__name__, static_folder='static/dist/', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/games")
def games():
    genre_filter = request.args.get("genre")
    platform_filter = request.args.get("platform")
    year_filter = request.args.get("year")
    sort_option = request.args.get("sort", "title")

    query = Game.query

    if genre_filter:
        query = query.filter(Game.genre == genre_filter)
    if platform_filter:
        query = query.filter(Game.platform == platform_filter)
    if year_filter:
        query = query.filter(db.extract('year', Game.release_date) == int(year_filter))

    if sort_option == "title":
        query = query.order_by(Game.title.asc())
    elif sort_option == "date_desc":
        query = query.order_by(Game.release_date.desc())
    elif sort_option == "date_asc":
        query = query.order_by(Game.release_date.asc())

    games = query.all()

    genres = db.session.query(Game.genre).distinct().order_by(Game.genre).all()
    platforms = db.session.query(Game.platform).distinct().order_by(Game.platform).all()
    years = db.session.query(db.extract('year', Game.release_date)).distinct().order_by(db.extract('year', Game.release_date).desc()).all()

    return render_template("games.html",
        games=games,
        genres=[g[0] for g in genres if g[0]],
        platforms=[p[0] for p in platforms if p[0]],
        years=[y[0] for y in years if y[0]],
    )

@app.route('/news')
def news_list():
    category = request.args.get("category")
    if category:
        news = News.query.filter_by(category=category).order_by(News.date_posted.desc()).all()
    else:
        news = News.query.order_by(News.date_posted.desc()).all()
    categories = db.session.query(News.category).distinct().all()
    return render_template("news.html", news=news, categories=[c[0] for c in categories if c[0]])


@app.route('/news/<int:news_id>')
def news_detail(news_id):
    article = News.query.get_or_404(news_id)
    return render_template('news_detail.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)