# Popcorn-Time_anime_localhost_server
This project is about Popcorn-Time. Currently, the official APIs are not able to provide anime data, this project might do the job.
# How to use
## Installation
flask module is needed for this repo</br>
`pip install flask`</br>
clone the repo</br>
`git clone https://github.com/TWTom041/Popcorn-Time_anime_localhost_server.git` </br>
fill the blanks in `auth_kitsu.json`</br>
######example:
```json
{
  "access_token": "1dxCxes5gnPkQV9juv2pxA2MU4gdlskcyROOCXKLwjA",
  "token_type": "Bearer",
  "expires_in": 2592000,
  "refresh_token": "5UjncPIvSKVeyQPy5kzl6zkKwew4mc8qPziY7eE19qQ",
  "scope": "public",
  "created_at": 1658066709
}
```
about how to get access_token and refresh_token, check the kitsu api docs</br>
<https://hummingbird-me.github.io/api-docs/#section/Authentication/Obtaining-an-Access-Token>
## Usage
cd to the directory where main.py is, and run the server like this</br>
`python main.py [port]`</br>
example:</br>
`python main.py 5000`</br>
the server api will be at localhost:5000/
# Known issue
1. Still not able to watch
# Todo
1. Make thing work
2. Database support
3. Other website support. (only kitsu api supported now)
