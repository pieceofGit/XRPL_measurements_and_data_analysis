"""A data analysis tool prototype for getting info about xrpl chain nodes.
Currently only analysis info about one node. """
import matplotlib.pyplot as plt
import json
import time
import sys

nodes = [{"host":"r.ripple.com", "port":"51234/"}]
with open("../data_collection/node_measurements.json", "r") as f:
    data = json.load(f)

def get_convergence_time():
    converge_time_list = [x["info"]["last_close"]["converge_time_s"] for x in data["r.ripple.com"]]
    print(min(converge_time_list))
    print(max(converge_time_list))
    plt.plot(converge_time_list)
    plt.ylabel("Convergence time (seconds)")
    plt.xlabel("Latest validated ledger")
    plt.show()

def get_peers():
    peers_list = [x["info"]["peers"] for x in data["r.ripple.com"]]
    proposers_list = [x["info"]["last_close"]["proposers"] for x in data["r.ripple.com"]]
    print(min(peers_list))
    print(max(peers_list))
    plt.plot(peers_list, label="number of peers")
    plt.plot(proposers_list, label="number of proposers")
    plt.legend()
    plt.ylabel("Number of nodes")
    plt.xlabel("Latest validated ledger")
    plt.show()

"""If the data is on a 15 minute interval, we have multiple writes."""

print(json.dumps(data["r.ripple.com"][0]))
print(sys.getsizeof(json.dumps(data["r.ripple.com"][0])))
# get_convergence_time()
get_peers()