import requests
import random
import json
# Used for fetching crawling data
PEER_PORT = "51235/"
# Used for fetching rippled server data
PUBLIC_PORT = "51234/"
HOST = "https://r.ripple.com"
# Request data
with open("crawl.json", "r") as f:
    response = json.load(f)
# print(len(response["overlay"]["active"]))

# # overlay, server, unl, version
success = 0
failed = 0
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
peers = response["overlay"]["active"]
random.shuffle(peers)
for active_peer in peers:
    try:
        active_peer_ip = active_peer["ip"][7::] if active_peer["ip"][0] == ":" else active_peer["ip"]
        print(active_peer_ip, active_peer["ip"])
        response = requests.get("https://"+active_peer_ip+":"+PUBLIC_PORT, timeout=2, verify=False, data=json.dumps({"method": "server_info"}))
        if response.status_code == 200:
            print(response, response.json())
        print(response)
        success += 1
    except Exception as e:
        print(e)
        failed += 1
print(success)
print(failed)


# def get_validators_from_node(self):
#     response = requests.get("https://"+self.validators_node, timeout=2, verify=False)
#     self.nodes = response.json()
#     self.nodes = json.loads(base64.b64decode(self.nodes["blob"]))
#     print("MANIFEST STUFF", self.nodes["validators"][0]["manifest"])
#     print(base64.b64decode(self.nodes["validators"][0]["manifest"]))

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

