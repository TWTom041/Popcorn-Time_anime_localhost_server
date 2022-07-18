from re import search
from requests import get
from bs4 import BeautifulSoup as bs

'''
[{
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
}]
'''


# scratch contents from acg.rip
def acgrip():
    pass


# scratch contents from nyaa.si
def nyaa(info):
    def beautifuler(data):
        data = data.find("table", class_="torrent-list").find("tbody").find_all("tr")
        res = []
        for i in data:
            foo = i.find_all("td")
            if foo[5].find(text=True) == "0":
                break
            res.append((lambda x: [
                [d.parent.find(text=True, recursive=False)[:-1] for d in  # .find(text=True, recursive=False)
                 bs(get("https://nyaa.si" + x[1].find("a")["href"]).text, 'html.parser').find_all("i", {"class": "fa-file"})],
                x[2].find_all("a")[1]["href"], int(x[5].find(text=True))])(foo))
            res[-1][0] = list(filter(lambda bar: bar.endswith((".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")) and all(item not in bar for item in ["SP", "ED", "OP"]), res[-1][0]))
            print(res[-1])
        print(res)
        return res

    title = (info["attributes"]["titles"]["en_jp"] if info["attributes"]["titles"].__contains__("en_jp") else
             info["attributes"]["titles"]["en"] if info["attributes"]["titles"].__contains__("en") else
             info["attributes"]["titles"]["ja_jp"] if info["attributes"]["titles"].__contains__("ja_jp") else
             list(info["attributes"]["titles"].values())[0]) if info["attributes"].__contains__(
        "titles") else "unknown"
    dat = {
        "en": beautifuler(
            bs(get("https://nyaa.si", params={"q": title, "f": "0", "s": "seeders", "c": "1_2", "o": "desc"}).text,
               "html.parser")),
        "nonen": beautifuler(
            bs(get("https://nyaa.si", params={"q": title, "f": "0", "s": "seeders", "c": "1_3", "o": "desc"}).text,
               "html.parser")),
        "raw": beautifuler(
            bs(get("https://nyaa.si", params={"q": title, "f": "0", "s": "seeders", "c": "1_4", "o": "desc"}).text,
               "html.parser"))
    }
    return dat


# make the list the right term
def refactor():
    pass


# return a list contains torrents' info
def get_torrent():
    pass
