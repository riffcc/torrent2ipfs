# torrent2ipfs
torrent2ipfs is a BitTorrent to IPFS bridge. It takes torrent files, downloads them with a torrent client and then adds the downloaded content to IPFS.

Requires IPFS, Python3, qBittorrent.

torrent2ipfs will add all torrents from ingest/ to qBittorrent with a special tag, then monitor qBittorrent until it no longer has any torrents to download. It will create IPFS hashes for each torrent you added, storing them as a JSON file. It's smart enough to skip creating IPFS hashes for torrents it has already processed before.

test.torrent is included for testing, which is actually ubuntu-20.04.4-live-server-amd64.iso.torrent

## Setup
You'll need to install some python libraries before running this.

```
pip3 install python-dotenv
pip3 install qbittorrent-api
pip3 install ipfshttpclient
pip3 install humanfriendly
```

You'll also need to create a configuration file. Copy `.env.dist` to `.env` and edit it.

You'll end up with something like this:
```
# Username
username=zorlin
# Password
password=mysecurepassword
# URL
url=qbittorrent.nasa.gov
# Port
port=443
# Label to use for adding and checking torrents
label=torrent2ipfs
```

## Usage
Place torrents to "convert" into ingest/, then run `python3 main.py`.
