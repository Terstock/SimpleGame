import requests
import os
from datetime import datetime
from models import db, Game
from app import app


CLIENT_ID = "mky6rhte59jj1ojfsio29z9w6rq2jg"
CLIENT_SECRET = "zkm7l9lifuoe29znzfikcjqoruoxd2"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"
IGDB_API_URL = "https://api.igdb.com/v4/games"



def get_access_token():
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    })
    response.raise_for_status()
    return response.json()['access_token']



def fetch_game_from_igdb(title):
    token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }

    query = f'search "{title}"; fields name,summary,cover.url,first_release_date,platforms.name,genres.name,involved_companies.company.name; limit 1;'
    response = requests.post(IGDB_API_URL, headers=headers, data=query)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else None



def add_game_from_igdb(titles):
    if isinstance(titles, str):
        titles = [titles]  

    for title in titles:
        game_data = fetch_game_from_igdb(title)
        if not game_data:
            print(f"❌ Гру '{title}' не знайдено.")
            continue

        name = game_data.get('name')
        description = game_data.get('summary', '')
        release_date = datetime.utcfromtimestamp(game_data.get('first_release_date', 0)).date() if game_data.get('first_release_date') else None
        developer = game_data.get('involved_companies', [{}])[0].get('company', {}).get('name', 'Unknown')
        genre = game_data.get('genres', [{}])[0].get('name', 'Unknown')
        platform = game_data.get('platforms', [{}])[0].get('name', 'Unknown')
        cover_image = "https://images.igdb.com/igdb/image/upload/t_cover_big/" + game_data.get('cover', {}).get('url', '').split('/')[-1] if game_data.get('cover') else ''

        with app.app_context():
            if not Game.query.filter_by(title=name).first():
                new_game = Game(
                    title=name,
                    description=description,
                    release_date=release_date,
                    developer=developer,
                    genre=genre,
                    platform=platform,
                    cover_image=cover_image
                )
                db.session.add(new_game)
                db.session.commit()
                print(f"✅ Гру '{name}' додано до бази даних.")
            else:
                print(f"ℹ️ Гра '{name}' вже існує в базі.")


def bulk_add_games(limit=200):
    token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }

    query = f'fields name,summary,cover.url,first_release_date,platforms.name,genres.name,involved_companies.company.name; sort popularity desc; limit {limit};'
    response = requests.post(IGDB_API_URL, headers=headers, data=query)
    response.raise_for_status()
    games = response.json()

    BLOCKED_GENRES = {'Erotic', 'Adult', 'Nudity', 'Hentai', 'Sexual Content'}

    with app.app_context():
        added_count = 0
        for game_data in games:
            name = game_data.get('name')
            description = game_data.get('summary', '')
            release_date = datetime.utcfromtimestamp(game_data.get('first_release_date', 0)).date() if game_data.get('first_release_date') else None
            developer = game_data.get('involved_companies', [{}])[0].get('company', {}).get('name', 'Unknown')

            genres = [g.get('name', '') for g in game_data.get('genres', [])]
            if any(g in BLOCKED_GENRES for g in genres):
                continue

            genre = genres[0] if genres else 'Unknown'

            platforms = [p.get('name', '') for p in game_data.get('platforms', [])]
            platform = platforms[0] if platforms else 'Unknown'

            cover_image = "https://images.igdb.com/igdb/image/upload/t_cover_big/" + game_data.get('cover', {}).get('url', '').split('/')[-1] if game_data.get('cover') else ''

            if not Game.query.filter_by(title=name).first():
                new_game = Game(
                    title=name,
                    description=description,
                    release_date=release_date,
                    developer=developer,
                    genre=genre,
                    platform=platform,
                    cover_image=cover_image
                )
                db.session.add(new_game)
                added_count += 1

        db.session.commit()
        print(f"✅ Додано {added_count} ігор до бази")