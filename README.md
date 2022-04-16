# torrent2ipfs
BitTorrent to IPFS bridge

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

## Usage
Place torrents to "convert" into ingest/, then run `python3 main.py`.
