# based on popcorn time 0.4.7
import sys

from flask import Flask, jsonify, request
import requests
from datetime import datetime
from time import mktime
from sys import argv

app = Flask(__name__)
app.config["DEBUG"] = True


# using kitsu.io's kitsu api
@app.route("/animes/<int:page>", methods=["GET"])
def animesGet(page):
    r = []
    for i in range(3):
        target = f"https://kitsu.io/api/edge/anime?page[limit]=20&page[offset]={(page - 1) * 50 + i * 20}&sort=-averageRating" if i != 2 else f"https://kitsu.io/api/edge/anime?page[limit]=10&page[offset]={(page - 1) * 50 + 40}&sort=-averageRating"
        target += f"&filter[text]={request.args['keywords']}" if "keywords" in request.args else ""
        data = requests.get(target).json()
        for s in data["data"]:
            tmp = {"_id": s["id"],
                   "mal_id": s["id"],
                   "imdb_id": s["id"],
                   "tmdb_id": s["id"],
                   "tvdb_id": s["id"],
                   "item_data": s["attributes"]["subtype"],
                   "title": (s["attributes"]["titles"]["ja_jp"] if s["attributes"]["titles"].__contains__("ja_jp") else
                             s["attributes"]["titles"]["en_jp"] if s["attributes"]["titles"].__contains__("en_jp") else
                             s["attributes"]["titles"]["en"] if s["attributes"]["titles"].__contains__("en") else
                             list(s["attributes"]["titles"].values())[0]) if s["attributes"].__contains__(
                       "titles") else "unknown",
                   "year": s["attributes"]["startDate"][:4] if s["attributes"][
                                                                   "startDate"] is not None else "?",
                   "slug": (s["attributes"]["titles"]["ja_jp"] if s["attributes"]["titles"].__contains__("ja_jp") else
                            s["attributes"]["titles"]["en_jp"] if s["attributes"]["titles"].__contains__("en_jp") else
                            s["attributes"]["titles"]["en"] if s["attributes"]["titles"].__contains__("en") else
                            list(s["attributes"]["titles"].values())[0]) if s["attributes"].__contains__(
                       "titles") else "unknown",
                   "type": "anime",
                   "original_language": "jp",
                   "exist_translations": ["jp"],
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
                   }
            r.append(tmp)

    return jsonify(r)


@app.route("/anime/<_id>", methods=["GET"])
def animeGet(_id):
    target = f"https://kitsu.io/api/edge/anime/{_id}"
    s = requests.get(target).json()["data"]
    return jsonify({
        "_id": s["id"],
        "mal_id": s["id"],
        "imdb_id": s["id"],
        "tmdb_id": s["id"],
        "tvdb_id": s["id"],
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
    return "TWTom's custom Popcorn Time server for anime"


if __name__ == "__main__":
    app.run(port=int(sys.argv[1]))
