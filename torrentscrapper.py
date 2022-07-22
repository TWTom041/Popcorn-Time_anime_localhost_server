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
        item not in bar for item in ["ED", "OP", "Ending", "Opening", "ending", "opening", "menu", "pv", "cm"]),
                         res[0]))
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
    def connector(title, mode, presubbed=True):
        mode_trans = {"en": "1_2", "nonen": "1_3", "raw": "1_4"}
        data = bs(get("https://nyaa.si",
                      params={"q": title, "f": "0", "s": "seeders", "c": mode_trans[mode], "o": "desc"}).text,
                  "html.parser")
        print(title)
        result = []
        try:
            data = data.find("table", class_="torrent-list").find("tbody").find_all("tr")
        except AttributeError:
            return result
        # data is torrent list in html
        for i in data:
            res = []
            # foo finds one torrent's name, magnet, seeds and whatever
            foo = i.find_all("td")
            # seeds == 0
            if foo[5].find(text=True) == "0":
                break
            res.append((lambda x: [
                bs(get("https://nyaa.si" + x[1].find("a")["href"]).text, 'html.parser'),
                x[2].find_all("a")[1]["href"], int(x[5].find(text=True))])(foo))
            # totaltitle is the title displayed on html
            totaltitle = res[-1][0].find("h3", class_="panel-title").text
            # this line will trans file names in html into file names
            res[-1][0] = [d.parent.find(text=True, recursive=False)[:-1] for d in
                          res[-1][0].find_all("i", {"class": "fa-file"})]
            # res[-1] = [[title1, title2...], magnet_link, seeds]
            parsed = parse(res[-1], "nyaa.si", "https://nyaa.si" + foo[1].find("a")["href"], info["id"], totaltitle,
                           presubbed)
            print("https://nyaa.si" + foo[1].find("a")["href"])
            print(parsed)
            for ep in parsed:
                if not result:
                    # the result is empty
                    result = parsed
                    break
                else:
                    # check which episode is parsed
                    tempflag = True  # if the current episode didn't do any thing to existed, then true
                    for existep in result:
                        if existep["season"] == ep["season"] and existep["episode"] == ep["episode"]:
                            # same file name
                            tempflag = False
                            if list(ep["torrents"].keys())[0] in existep["torrents"].keys():
                                # same resolution and file name
                                print("same file")
                            else:
                                # same file name but resolution
                                print("did it")
                                result[result.index(existep)]["torrents"] = result[result.index(existep)]["torrents"] | \
                                                                            ep["torrents"]
                            break
                    if tempflag:
                        # another episode
                        print("diditwlelel")
                        result.append(ep)
                    else:
                        print("somethings wrong")

            if len(parsed) >= 3:
                # it's compilation
                break

        return result

    def beautifuler(title, mode, presubbed=True):
        fnresult = connector(title, mode, presubbed)
        s_e = []
        # s_e = [[season, {episode, episode...}], [season, {episode, episode}]...]
        for epi in fnresult:
            if epi["season"] not in [x[0] for x in s_e]:
                s_e.append([epi["season"], {epi["episode"]}])
            else:
                for sets in s_e:
                    if sets == epi["season"]:
                        s_e[s_e.index(sets)][1].add(epi["episode"])
        # find whole season missing
        missing_s = sorted(set(range(1, sorted([t[0] for t in s_e])[-1]+1)) - set([t[0] for t in s_e]))
        for season in missing_s:
            fnresult += connector(title+f" s{season}", mode, presubbed)
        # check if the anime is still going
        target = sorted([t[0] for t in s_e])[-1]
        while True:
            target += 1
            tmpres = connector(title+f" s{target}", mode, presubbed)
            if not tmpres:
                break
            fnresult += tmpres

        print("ssss", fnresult)
        return fnresult
        pass

    title1 = (info["attributes"]["titles"]["en_jp"] if info["attributes"]["titles"].__contains__("en_jp") else
              info["attributes"]["titles"]["en"] if info["attributes"]["titles"].__contains__("en") else
              info["attributes"]["titles"]["ja_jp"] if info["attributes"]["titles"].__contains__("ja_jp") else
              list(info["attributes"]["titles"].values())[0]) if info["attributes"].__contains__(
        "titles") else "unknown"
    # dat = {
    #     "en": beautifuler(title1, "en"),
    #     "nonen": beautifuler(title1, "nonen"),
    #     "raw": beautifuler(title1, "raw")
    # }
    dat = {
        "episodes": beautifuler(title1, "en")
    }
    return dat


# return a list contains torrents' info
def get_torrent():
    pass


if __name__ == "__main__":
    nyaa({"id": 1277, "attributes": {"titles": {"en_jp": "Go toubun no Hanayome"}}})
