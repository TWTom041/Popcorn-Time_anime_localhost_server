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


# parse raw datas into readable
def parse(res, provider, source, tvbd_id):
    # res = [titles, torrent_url, seeds]
    result = []
    res[0] = list(filter(lambda bar: bar.endswith((".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")) and all(
        item not in bar for item in ["ED", "OP", "Ending", "Opening", "ending", "opening"]), res[0]))
    season = 1
    while any(f"S{season:02}" in titl for titl in res[0]):
        episode = 0
        for titl in res[0]:
            if f"S{season:02}" in titl:
                while True:
                    episode += 1
                    if f"S{season:02}E{episode:02}" in titl:
                        result.append({"databased": False,
                                       "season": season,
                                       "episode": episode,
                                       "first_aired": 1,
                                       "title": f"Episode {episode}",
                                       "overview": "not supported yet",
                                       "watched": {"watched": False},
                                       "tvbd_id": tvbd_id,
                                       "torrents": {
                                           "1080p" if any(key in titl.lower() for key in [
                                               "1080", "fhd", "full hd", "fullhd", "full-hd", "full.hd"]) else
                                           "720p" if any(key in titl.lower() for key in [
                                               "720"]) else
                                           "480p" if any(key in titl.lower() for key in [
                                               "480", "shd"]) else
                                           "2160p" if any(key in titl.lower() for key in [
                                               "4k", "2160p", "uhd", "ultra hd", "ultrahd"]) else
                                           "0": {
                                               "url": res[1], "provider": provider,
                                               "source": source,
                                               "title": titl, "seeds": res[2], "peers": res[2],
                                               "file": titl}
                                       }})
                        result[-1]["torrents"][list(result[-1]["torrents"].keys())[-1]]["quality"] = \
                            list(result[-1]["torrents"].keys())[-1]
                    else:
                        break
        season += 1
    return result

# scratch contents from acg.rip
def acgrip():
    pass


# scratch contents from nyaa.si
def nyaa(info):
    def beautifuler(data):
        data = data.find("table", class_="torrent-list").find("tbody").find_all("tr")
        result = []
        for i in data:
            res = []
            foo = i.find_all("td")
            if foo[5].find(text=True) == "0":
                break
            res.append((lambda x: [
                [d.parent.find(text=True, recursive=False)[:-1] for d in  # .find(text=True, recursive=False)
                 bs(get("https://nyaa.si" + x[1].find("a")["href"]).text, 'html.parser').find_all("i", {
                     "class": "fa-file"})],
                x[2].find_all("a")[1]["href"], int(x[5].find(text=True))])(foo))
            result = parse(res[-1], "nyaa.si", "https://nyaa.si" + foo[1].find("a")["href"], info["id"])
            print()
            print(result)
        return result

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


if __name__ == "__main__":
    nyaa({"id": 1277, "attributes": {"titles": {"en_jp": "Go toubun no Hanayome"}}})
