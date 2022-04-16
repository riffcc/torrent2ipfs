#!/usr/bin/python3
# Load various libraries
from dotenv import load_dotenv
from qbittorrentapi import Client
from humanfriendly import format_timespan

import os
import json
import ipfshttpclient

print("torrent2ipfs starting... let's get interplanetary.")

# Load .env
load_dotenv()

# Set variables based on what we pulled from .env
username = os.getenv('username')
password = os.getenv('password')
url = os.getenv('url')
port = os.getenv('port')
label = os.getenv('label')

# Load existing database of pairs
if(os.path.isfile("pairs.json")):
    pairs = json.load(open("pairs.json"))
else:
    pairs = {}

print("[Stage 1] Setting up connections.")
print("Connecting to qBittorrent...")
# Spawn a qbt_client object to interact with
qbt_client = Client(host=url + ":" + port, username=username, password=password)

print("Connecting to IPFS daemon...")
# Spawn an IPFS client object to interact with
ipfs_client = ipfshttpclient.connect()

print("[Stage 2] Importing torrents from ingest/ folder.")
# Get a list of torrents in the ingest folder, then load them into qBT
for torrent in os.scandir('ingest/'):
    if torrent.is_file():
        print("Adding torrent " + torrent.name)
        qbt_client.torrents_add(torrent_files=open('ingest/' + torrent.name, "rb"), tags=label)

finished = False

while finished == False:
    print("[Stage 3A] Checking downloads in progress...")
    # Grab a list of downloading torrents from qBittorrent
    torrents_info = qbt_client.torrents_info(status_filter="downloading", tag=label)

    print("Currently downloading " + str(len(torrents_info)) + " torrents.")

    if len(torrents_info) != 0:
        for torrent in torrents_info:
            print(torrent["hash"] + ": estimated time remaining: " + format_timespan(torrent["eta"]))
    else:
        finished = True

    print("[Stage 3B] Adding completed torrents to IPFS.")

    # Grab a list of completed/seeding torrents from qBittorrent
    torrents_info = qbt_client.torrents_info(status_filter="completed", tag=label)
    if len(torrents_info) == 0:
        print("No completed torrents found yet.")
    # For each completed torrent...
    for completed_torrent in torrents_info:
        # Check if the info_hash is in our list of pairs
        if(completed_torrent["hash"] in pairs):
            #print("Found IPFS hash for " + completed_torrent["hash"] + ":")
            #print("ipfs://" + pairs[completed_torrent["hash"]])
            pass
        # If it is not...
        else:
            print("Torrent not in IPFS yet: " + completed_torrent["hash"])
	    # Add it to IPFS
            print("Adding to IPFS...")
            if os.path.isdir(completed_torrent["content_path"]):
                res = ipfs_client.add(completed_torrent["content_path"], recursive=True)
                # and store the IPFS hash in our array.
                print("New IPFS hash: " + res[0]["Hash"])
                pairs[completed_torrent["hash"]] = res[0]["Hash"]
            else:
                res = ipfs_client.add(completed_torrent["content_path"])
                print("New IPFS hash: " + res["Hash"])
                pairs[completed_torrent["hash"]] = res["Hash"]

print("Finished.")
print("Writing pairs.json with all discovered hashes.")

# Write database of pairs
json.dump(pairs, open("pairs.json", 'w'))
