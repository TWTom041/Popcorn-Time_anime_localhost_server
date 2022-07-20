import re
from requests import get
from bs4 import BeautifulSoup as bs


# parse raw datas into readable
def parse(res, provider, source, tvdb_id, totaltitle, presubbed=True):
    # res = [titles, torrent_url, seeds]
    def uniout(season, episode, quality, url, seeds, file):
        return {"date_based": False,
                "season": season,
                "episode": episode,
                "first_aired": 1,
                "title": f"Episode {episode}",
                "overview": "not supported yet",
                "watched": {"watched": False},
                "tvdb_id": tvdb_id,
                "torrents": {
                    quality: {
                        "url": url,
                        "provider": provider,
                        "source": source,
                        "title": file,
                        "quality": quality,
                        "seeds": seeds,
                        "peers": seeds + 1,
                        "file": file,
                        "presubbed": presubbed
                    }
                }}

    result = []
    # res[0] = [title1, title2.....]
    res[0] = list(filter(lambda bar: bar.endswith((".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")) and all(
        item not in bar for item in ["ED", "OP", "Ending", "Opening", "ending", "opening", "menu"]), res[0]))
    for titl in res[0]:
        quality = "1080p" if any(
            chk in totaltitle.lower() for chk in ["1080", "fhd", "fullhd", "full hd", "full.hd"]) else \
            "720p" if any(chk in totaltitle.lower() for chk in ["720"]) else \
                "2160p" if any(
                    chk in totaltitle.lower() for chk in ["2160", "uhd", "ultra hd", "ultrahd", "ultra.hd", "4k"]) else \
                    "480p" if any(chk in totaltitle.lower() for chk in ["480", "shd"]) else "0"
        # search for SxxExx type title
        pattern = re.compile(r's([0-9]{2})e([0-9]{2})')
        sresult = re.search(pattern, titl.lower())
        if sresult is not None:
            s_e = (int(sresult.group(1)), int(sresult.group(2)))
            result.append(uniout(s_e[0], s_e[1], quality, res[1], res[2], titl))
            continue
        # search for Sx/Sxx for season xx for episode
        pattern = re.compile(r's[0-9]{2}|s[0-9]')
        sresult = re.search(pattern, titl.lower())
        if sresult is None:
            pattern = re.compile(r"\D(\d\d)\D")
            eresult = int(re.findall(pattern, titl)[0])
            result.append(uniout(1, eresult, quality, res[1], res[2], titl))
        else:
            sresult = sresult.group()
            pattern = re.compile(r"\D(\d\d)\D")
            eresult = int(re.findall(pattern, titl.replace(sresult, ""))[0])
            result.append(uniout(int(sresult[1:]), eresult, quality, res[1], res[2], titl))

    return result


# scratch contents from acg.rip
def acgrip():
    pass


# scratch contents from nyaa.si
def nyaa(info):
    def beautifuler(title, mode, presubbed=True, wf=False):
        mode_trans = {"en": "1_2", "nonen": "1_3", "raw": "1_4"}
        data = bs(get("https://nyaa.si",
                      params={"q": title, "f": "0", "s": "seeders", "c": mode_trans[mode], "o": "desc"}).text,
                  "html.parser")
        data = data.find("table", class_="torrent-list").find("tbody").find_all("tr")
        result = []
        undone = []
        for i in data:
            res = []
            foo = i.find_all("td")
            if foo[5].find(text=True) == "0":
                break
            res.append((lambda x: [
                bs(get("https://nyaa.si" + x[1].find("a")["href"]).text, 'html.parser'),
                x[2].find_all("a")[1]["href"], int(x[5].find(text=True))])(foo))
            totaltitle = res[-1][0].find("h3", class_="panel-title").text
            res[-1][0] = [d.parent.find(text=True, recursive=False)[:-1] for d in
                          res[-1][0].find_all("i", {"class": "fa-file"})]
            # res[-1] = [[title1, title2...], magnet_link, seeds]
            for ep in parse(res[-1], "nyaa.si", "https://nyaa.si" + foo[1].find("a")["href"], info["id"], totaltitle,
                           presubbed):
                if result == []:
                    result = parse(res[-1], "nyaa.si", "https://nyaa.si" + foo[1].find("a")["href"], info["id"],
                                   totaltitle,
                                   presubbed)
                else:
                    pass

            if len(result) >= 3:
                if not wf:
                    print("com")
                    # it's compilation
                    # check what seasons are missing
                    containedseason = sorted(list(set([i["season"] for i in result])))
                    for n in range(containedseason[-1]):
                        if n not in containedseason:
                            undone.append(n)
                    for season in undone:
                        beautifuler(f"{title} s{season}", mode, wf=True)
                    break
                else:
                    # the work done in second lap
                    pass
            print("https://nyaa.si" + foo[1].find("a")["href"])
            print(result)
        return result

    title1 = (info["attributes"]["titles"]["en_jp"] if info["attributes"]["titles"].__contains__("en_jp") else
              info["attributes"]["titles"]["en"] if info["attributes"]["titles"].__contains__("en") else
              info["attributes"]["titles"]["ja_jp"] if info["attributes"]["titles"].__contains__("ja_jp") else
              list(info["attributes"]["titles"].values())[0]) if info["attributes"].__contains__(
        "titles") else "unknown"
    dat = {
        "en": beautifuler(title1, "en"),
        "nonen": beautifuler(title1, "nonen"),
        "raw": beautifuler(title1, "raw")
    }
    return dat


# return a list contains torrents' info
def get_torrent():
    pass


if __name__ == "__main__":
    nyaa({"id": 1277, "attributes": {"titles": {"en_jp": "Go toubun no Hanayome"}}})
