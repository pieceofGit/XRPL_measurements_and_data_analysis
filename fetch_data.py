import requests
import random
import json
# Used for fetching crawling data
PEER_PORT = "51235/"
# Used for fetching rippled server data
PUBLIC_PORT = "51234/"
HOST = "https://r.ripple.com"
# Request data
# with open("crawl.json", "r") as f:
#     response = json.load(f)
# print(len(response["overlay"]["active"]))
response = requests.get(HOST+":"+PUBLIC_PORT, timeout=2, verify=False, data=json.dumps({"method": "server_info","params": [{}]})).json()
print(response)
# # overlay, server, unl, version
# success = 0
# failed = 0
# peers = response["overlay"]["active"]
# random.shuffle(peers)
# for active_peer in peers[0::10]:
#     try:
#         response = requests.get("http://"+active_peer["ip"]+":"+PEER_PORT+"health", timeout=2, verify=False)
#         success += 1
#     except Exception as e:
#         print(e)
#         failed += 1
# print(success)
# print(failed)

# # Setup pipeline for storing data. 
# # Data should be stored in database with time and public key

# # result: { info: { build_version, io_latency_ms, last_close: { converge time, proposers }, pubkey_node, peers }, uptime, status }

# # Store in database

# # Should the prototype do something specific?
# # Part one: Data storage 
# # Part two: Data analysis

# # Walkthrough
# # Data storage
# # Gets data from all nodes on an interval (not exceeding too many requests) 
#     # Data should be either stored on average over some x requests or store every request.
#     # The data should be indexable by public key and time.
# # Data analysis
# # Creates analytics from the stored data
#     # Should create graphs based on input
#     # Give outlier data and change based on each parameter
#     # Should be able to make analytics and get a csv file for example in a third party.

