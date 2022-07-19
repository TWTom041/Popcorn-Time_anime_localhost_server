# based on popcorn time 0.4.7
from flask import Flask, jsonify, request
import requests
from datetime import datetime
from time import mktime, time
from sys import argv
import json
from urllib import parse
from ast import literal_eval

app = Flask(__name__)
app.config["DEBUG"] = True
sort = {"seeds": "-averageRating",
        "name": "-titles",
        "year": "-startDate"}
'''
genres:
    'All',
    'Action',
    'Adventure',
    'Cars',  not available
    'Comedy',
    'Dementia',
    'Demons',  not available
    'Drama',
    'Ecchi',
    'Fantasy',
    'Game',  not available
    'Harem',
    'Historical',
    'Horror',
    'Josei',
    'Kids',  few contents
    'Magic',
    'Martial Arts',
    'Mecha',
    'Military',
    'Music',
    'Mystery',
    'Parody',
    'Police',  not available
    'Psychological',
    'Romance',
    'Samurai',
    'School',
    'Sci-Fi',  not available
    'Seinen',
    'Shoujo',
    'Shoujo Ai',
    'Shounen',
    'Shounen Ai',
    'Slice of Life',
    'Space',
    'Sports',
    'Super Power',
    'Supernatural',
    'Thriller',
    'Vampire'
'''


def acckitsu(url, method="get"):
    if method == "get":
        tmp = open("auth_kitsu.json", 'r')
        f = json.load(tmp)
        tmp.close()
        if time() >= f['created_at'] + f["expires_in"]:
            re = requests.post("https://kitsu.io/api/oauth/token",
                               headers={"Content-Type": "application/x-www-form-urlencoded"}, data=parse.urlencode({
                    "grant_type": 'refresh_token',
                    "refresh_token": f['refresh_token']
                }))
            f = open("auth_kitsu.json", "w")
            json.dump(re.json(), f)
            f.close()
        with open("auth_kitsu.json", 'r') as tmp:
            f = json.load(tmp)
            r = requests.get(url, headers={"Authorization": f"Bearer {f['access_token']}"})
        return r.json()


# using kitsu.io's kitsu api
@app.route("/animes/<int:page>", methods=["GET"])
def animesGet(page):
    r = []
    for i in range(3):
        target = f"https://kitsu.io/api/edge/anime?page[limit]=20&page[offset]={(page - 1) * 50 + i * 20 if i != 2 else (page - 1) * 50 + 40}"
        target += f"&filter[text]={request.args['keywords']}" if "keywords" in request.args else ""
        target += f"&sort={sort[request.args['sort'] if 'sort' in request.args else 'seeds']}"
        target += f"&filter[categories]={request.args['genre']}" if 'genre' in request.args and request.args[
            'genre'] != "All" else ''
        data = acckitsu(target)
        for s in data["data"]:
            tmp = {"_id": s["id"],
                   "mal_id": s["id"],  # not yet supported
                   "imdb_id": s["id"],  # not yet supported
                   "tmdb_id": s["id"],  # not yet supported
                   "tvdb_id": s["id"],  # not yet supported
                   "item_data": s["attributes"]["subtype"],
                   "title": (s["attributes"]["titles"]["ja_jp"] if s["attributes"]["titles"].__contains__("ja_jp") else
                             s["attributes"]["titles"]["en_jp"] if s["attributes"]["titles"].__contains__("en_jp") else
                             s["attributes"]["titles"]["en"] if s["attributes"]["titles"].__contains__("en") else
                             list(s["attributes"]["titles"].values())[0]) if s["attributes"].__contains__(
                       "titles") else "unknown",
                   "year": s["attributes"]["startDate"][:4] if s["attributes"][
                                                                   "startDate"] is not None else "?",
                   "slug": s["attributes"]["slug"] if "slug" in s["attributes"] else "?",
                   "type": "anime",
                   "original_language": "jp",
                   "exist_translations": ["jp"],
                   "genres": ["Comedy"],
                   "images": {
                       "banner": s['attributes']['coverImage']['original'],
                       "fanart": s['attributes']['coverImage']['original'],
                       "poster": s["attributes"]["posterImage"]["original"]
                   } if s['attributes']['coverImage'] is not None else {},
                   "rating": {
                       "hated": 100,
                       "loved": 100,
                       "votes": 0,
                       "watching": 0,
                       "percentage": int(float(s["attributes"]["averageRating"])) if s["attributes"][
                                                                                         "averageRating"] is not None else 0
                   }
                   }
            r.append(tmp)

    return jsonify(r)


@app.route("/anime/<_id>", methods=["GET"])
def animeGet(_id):
    target = f"https://kitsu.io/api/edge/anime/{_id}"
    s = requests.get(target).json()["data"]
    return jsonify({
        "_id": s["id"],
        "mal_id": s["id"],  # not yet supported
        "imdb_id": s["id"],  # not yet supported
        "tmdb_id": s["id"],  # not yet supported
        "tvdb_id": s["id"],  # not yet supported
        "title": (s["attributes"]["titles"]["ja_jp"] if s["attributes"]["titles"].__contains__("ja_jp") else
                  s["attributes"]["titles"]["en_jp"] if s["attributes"]["titles"].__contains__("en_jp") else
                  s["attributes"]["titles"]["en"] if s["attributes"]["titles"].__contains__("en") else
                  list(s["attributes"]["titles"].values())[0]) if s["attributes"].__contains__(
            "titles") else "unknown",
        "year": s["attributes"]["startDate"][:4] if s["attributes"]["startDate"] is not None else "?",
        "original_language": "jp",
        "exist_translations": ["jp"],
        "slug": s["attributes"]["slug"] if s["attributes"]["slug"] is not None else "?",
        "contextLocale": "jp",
        "network": "whatever company",
        "synopsis": s["attributes"]["synopsis"],
        "runtime": str(s["attributes"]["episodeLength"]),
        "status": s["attributes"]["status"],
        "type": "anime",
        "country": 'Japan',
        "item_data": s["attributes"]["subtype"],
        "num_seasons": 1,
        "last_updated": int(
            mktime(datetime.strptime(s["attributes"]["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())),
        "__v": 0,
        "episodes": [{
            "data_based": False,
            "title": "Episode 13",
            "torrents": {
                "0": {
                    "url": "magnet:?xt=urn:btih:IEQGMZOUZJQ5FJJZNURKTTND3KUHBAHT&tr=http://open.nyaatorrents.info:6544/announce&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80/announce",
                    "seeds": 0,
                    "peers": 0,
                    "provider": "HorribleSubs"
                },
                "480p": {
                    "url": "magnet:?xt=urn:btih:IEQGMZOUZJQ5FJJZNURKTTND3KUHBAHT&tr=http://open.nyaatorrents.info:6544/announce&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80/announce",
                    "seeds": 0,
                    "peers": 0,
                    "provider": "HorribleSubs"
                },
                "720p": {
                    "url": "magnet:?xt=urn:btih:MCZBSUZP4YX2O4SBMBBXLFWBIQCEPOZF&tr=http://open.nyaatorrents.info:6544/announce&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80/announce",
                    "seeds": 0,
                    "peers": 0,
                    "provider": "HorribleSubs"
                }
            },
            "season": "1",
            "episode": "13",
            "overview": "We still don't have single episode overviews for anime… Sorry",
            "tvdb_id": "5646-1-13"
        }],
        "genres": ["Comedy"],
        "images": {
            "banner": s['attributes']['coverImage']['original'],
            "fanart": s['attributes']['coverImage']['original'],
            "poster": s["attributes"]["posterImage"]["large"]
        } if s['attributes']['coverImage'] is not None else {},
        "rating": {
            "hated": 100,
            "loved": 100,
            "votes": 0,
            "watching": 0,
            "percentage": int(float(s["attributes"]["averageRating"])) if s["attributes"][
                                                                              "averageRating"] is not None else 0
        }
    })


@app.route("/anime/undefined")
def rt():
    return "123123"


@app.route("/status")
def status():
    return '{"repo": "custom","server": "custom","status": "unknown","totalAnimes": 99999,"totalMovies": 0,"totalShows": 0,"updated": 1470233725,"uptime": 9,"version": "2.1.0","commit": "1212121"}'


@app.route("/logs/error")
def log():
    return ""


@app.route("/export/<collection>")
def export(collection):
    return "feature undone"


@app.route("/")
def home():
    return "custom Popcorn Time server for anime"


if __name__ == "__main__":
    app.run(port=int(argv[1]) if len(argv) > 2 else 5000)
