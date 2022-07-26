# Popcorn-Time_anime_localhost_server
This project is about Popcorn-Time. Currently, the official APIs are not able to provide anime data, this project might do the job.
# How to use
## Installation
1. clone the repo</br>
`git clone https://github.com/TWTom041/Popcorn-Time_anime_localhost_server.git` </br>
2. install the required modules for this repo</br>
`pip install requirements.txt`</br>
3. complete `auth_kitsu.json`</br>
example:
```json
{
  "access_token": "1dxCxes5gnPkQV9juv2pxA2MU4gdlskcyROOCXKLwjA",
  "token_type": "Bearer",
  "expires_in": 2592000,
  "refresh_token": "5UjncPIvSKVeyQPy5kzl6zkKwew4mc8qPziY7eE19qQ",
  "scope": "public",
  "created_at": 1658001009
}
```
4. go to the root of Popcorn Time App, which is usually at `%appdata%/Local/Popcorn-Time`</br>
5. edit `/src/app/lib/views/browser/item.js` into:</br>
```javascript
...
// around line 221:
showDetail: function (e) {
            e.preventDefault();

            var realtype = this.model.get('type');
            var itemtype = realtype.replace('bookmarked', '');
            var providerType = itemtype === 'show' ? 'tvshow' : itemtype;
            var providers = {torrent:App.Config.getProviderForType(providerType)[0]};
            // ----------new added------------
            // I don't know why but these lines worked for me
            $(".spinner").show();
            var temp = this.model;
            if (this.model.get("anime") || true) {
                    $.ajax({
                            url: "http://127.0.0.1:5000/anime/"+this.model.get("_id"),
                            type: 'GET',
                            async: false,
                            cache: false,
                            timeout: 60000,
                            error: function(){
                            $(".spinner").hide();
                            return true;},
                            success: function(msg){
                                    console.log(temp);
                                    var obj3 = {};
                                    msg = JSON.parse(JSON.stringify(msg))
                                    for (var attrname in temp["attributes"]) { obj3[attrname] = temp["attributes"][attrname]; }
                                    console.log(obj3["torrents"]);
                                    for (var attrname in msg) { obj3[attrname] = msg[attrname]; }
                                    console.log(obj3);
                                    temp.attributes = obj3;
                                    console.log(temp);
                            }
                    })
                    $(".spinner").hide();
            }
            console.log(this.model);
		//----------added end--------------
		this.model.set('providers', providers);
            var id = this.model.get(this.model.idAttribute);

            var promises = Object.values(providers).map(function (p) {
              if (realtype === 'show') {
                p = providers.torrent;
              }
                if (!p.detail) {
                    return false;
                }
                return p.detail(id, this.model.attributes);
            }.bind(this));
...
```
about how to get access_token and refresh_token, check the kitsu api docs:</br>
<https://hummingbird-me.github.io/api-docs/#section/Authentication/Obtaining-an-Access-Token>
## Usage
cd to the directory where main.py is, and run the server like this</br>
`python main.py [port]`</br>
example:</br>
`python main.py 5000`</br>
the server api will be at localhost:5000/</br>
then go to Popcorn Time's settings, change the anime api to http://localhost:5000/ or http://127.0.0.1:5000/ </br>
and the anime is now watchable
# Known issue
1. "sometimes" torrent scrapper might not work
2. Popcorn Time will lag a long bit to wait for the localhost server to load
# Todo
1. Database support
2. Other website support. (only kitsu api supported now)
