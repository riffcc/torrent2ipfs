#!/usr/bin/python3
# Load various libraries
from dotenv import load_dotenv
import xmlrpc.client
import os

# Load .env
load_dotenv()

# Set variables based on what we pulled from .env
protocol = os.getenv('proto')
username = os.getenv('username')
password = os.getenv('password')
url = os.getenv('url')
path = os.getenv('path')
port = os.getenv('port')
label = os.getenv('label')

# Create an XMLRPC to represent our rTorrent server
server_url = protocol + "://" + username + ":" + password + "@" + url + ":" + port + path
server = xmlrpc.client.Server(server_url)

server.load_start_verbose("test.torrent")

# Get torrents in the main view
mainview = server.download_list("", "main")

# For each torrent in the main view
for torrent in mainview:
    if server.d.custom1(torrent) == label:
        # Print the name of torrent
        print(server.d.get_name(torrent))
        print(server.d.custom1(torrent))
