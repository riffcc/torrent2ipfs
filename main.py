#!/usr/bin/python3
# Load various libraries
from dotenv import load_dotenv
from qbittorrentapi import Client

import os
import json
import ipfsApi

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

# Spawn a qbt_client object to interact with
qbt_client = Client(host=url + ":" + port, username=username, password=password)

# Spawn an IPFS client object to interact with
api = ipfsApi.Client('127.0.0.1', 5001)

# Get a list of torrents in the ingest folder, then load them into qBT
for torrent in os.scandir('ingest/'):
    if torrent.is_file():
        print(torrent.name)
        qbt_client.torrents_add(torrent_files=open('ingest/' + torrent.name, "rb"), tags=label)

#pairs = {"b44a0e20fa5b7cecb77156333b4268dfd7c30afb": "bar", "0cb7144515936e81f9d21d86af30f0627e02818a": "foo"}
pairs = {"foo": "bar", "bar": "foo"}

# For each completed torrent
torrents_info = qbt_client.torrents_info(status_filter="completed", tag=label)
for completed_torrent in torrents_info:
    print(completed_torrent["hash"])
    # Check if the info_hash is in our list of pairs
    if(completed_torrent["hash"] in pairs):
        print(pairs[completed_torrent["hash"]])
    # If it is not...
    else:
        res = api.add(completed_torrent["content_path"])
        print(res)

# Write database of pairs
json.dump(pairs, open("pairs.json", 'w'))