from threading import Thread
import json
import requests
import time
import urllib3
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""Currently a prototype storing data in json and only requesting data from one node"""
class DataCollector:
    """Periodically requests data about all nodes on XRPL nodes and stores in database"""
    def __init__(self, interval=60*15) -> None:
        self.nodes = None
        self.interval = interval
        self.public_port = "51234"
        self.peer_port = "51235"
        self.crawl_node = "r.ripple.com"
        self.validators_node = "vl.ripple.com"
        with open("node_measurements.json", "r") as f:
            self.data = json.load(f)
        with open("connected_nodes.json", "r") as f:
            self.connected_nodes = json.load(f)
        self.server_info_req = json.dumps({"method": "server_info", "params": [{}]})
        self.server_state_req = json.dumps({"method": "server_state", "params": [{}]})
    
    def persist_data(self) -> None:
        """Persists data in json file"""
        try:
            with open("node_measurements.json", "w+") as f:
                json.dump(self.data, f, indent=4)
                
            with open("connected_nodes.json", "w+") as f:
                json.dump(self.connected_nodes, f, indent=4)
                
        except Exception as e:
            print("Could not store data: ", e)
            

    def get_peers(self):
        """Fetches all 'active' nodes on the P2P overlay network"""
        # try:
        response = requests.get("https://"+"r.ripple.com:"+self.peer_port+"/crawl", timeout=2, verify=False)
        json_response = response.json()
        
        self.nodes = json_response["overlay"]["active"]
        # except Exception as e:
        #     print(e)

    # def get_validators(self):
    #     """Returns list of validators of nodes through peer_port/v1/{public_key} for each node"""
    #     for peer in self.peers:
    #         try:
    #             json_response = requests.get("https://"+peer["ip"]+":"+self.peer_port, timeout=2, verify=False).json()
    #         except Exception as e:
    #             print(e)
    def get_ipv4(self, ip):
        if len(ip) > 15:
            return ip[7::]
        return ip
        
    
    def fetch_data(self) -> None:
        """Periodically fetches data from nodes based on an interval"""
        self.get_peers()
        while True:
            for node in self.nodes:
                    try:
                        # Node may not have registered ip or were unable to connect
                        if not node.get("ip") in self.connected_nodes or self.connected_nodes[node["ip"]].get("connected") == True:    # Only fetch data from already connected or new nodes.
                            response_obj = requests.get("https://"+self.get_ipv4(node["ip"])+":"+self.public_port,
                                                    timeout=2, 
                                                    verify=False, 
                                                    data=self.server_state_req)
                            print(response_obj.status_code)
                            response = response_obj.json()
                            print("RESPONSE SUCCESS")
                            self.connected_nodes.setdefault(node["ip"], {"connected": True})
                            self.connected_nodes.setdefault(node["ip"], {"server_state": response["result"]["state"]["server_state"]})
                            self.data.setdefault(node["ip"], []).append(response["result"])
                            self.connected_nodes[node["ip"]]["count_success"] = self.connected_nodes[node["ip"]].get("count_success", 0) + 1
                            print("SUCCESS")
                    except Exception as e:
                        if "ip" in node:
                            self.connected_nodes.setdefault(node["ip"],  {"connected": False})
                            
                        print("Could not fetch data: ", e)
            self.persist_data()        
            time.sleep(self.interval)

data_collector = DataCollector()
data_collector.fetch_data()
# collector_thread = Thread(target=data_collector.fetch_data, name="DataCollectorThread")
# collector_thread.start()
# print(collector_thread.name)
# collector_thread.join()


# Get all nodes, check if success, then connect. 