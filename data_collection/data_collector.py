import base64
import json
import time
from threading import Thread

import requests
import urllib3

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
            self.con_nodes = json.load(f)
        self.server_info_req = json.dumps({"method": "server_info", "params": [{}]})
        self.server_state_req = json.dumps({"method": "server_state", "params": [{}]})
    
    def persist_data(self) -> None:
        """Persists data in json file"""
        try:
            with open("node_measurements.json", "w+") as f:
                json.dump(self.data, f, indent=4)
                
            with open("connected_nodes.json", "w+") as f:
                json.dump(self.con_nodes, f, indent=4)
                
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
        """Returns ip addresses in ipv4 format"""
        if len(ip) > 15:
            return ip[7::]
        return ip
        
    def get_ports(self, node):
        """Returns default ports or connected port"""
        ports = ["51234", "51235", "2459"]
        if "ip" in node:
            if self.con_nodes.get(node["ip"], {}).get("port", 0):
                return [self.con_nodes["ip"]["port"]]
            if "port" in node:
                ports.append(str(node["port"]))
            return ports
        return []
           
    def fetch_data(self) -> None:
        """Periodically fetches data from nodes based on an interval"""
        self.get_peers()
        while True:
            for node in self.nodes:
                # Node may not have registered ip or were unable to connect
                # Either connected node on specific port, or need to check all ports
                ports = self.get_ports(node)
                connected = False
                for port in ports:
                    try:
                        response_obj = requests.get("https://"+self.get_ipv4(node["ip"])+":"+port,
                                                timeout=2, verify=False, data=self.server_state_req)
                        if response_obj.status_code == 200:
                            response = response_obj.json()["result"]
                            connected = True
                            self.con_nodes.setdefault(node["ip"], {"connected": True})
                            self.con_nodes.setdefault(node["ip"], {"server_state": response["state"]["server_state"]})
                            self.data.setdefault(node["ip"], []).append(response)
                            self.con_nodes[node["ip"]]["count_success"] = self.con_nodes[node["ip"]].get("count_success", 0) + 1
                            print("SUCCESS", port)
                            break
                        if len(ports) == 1:
                            self.con_nodes[node["ip"]]["count_failures"] = self.con_nodes[node["ip"]].get("count_failures", 0) + 1
                        
                    except Exception as e:
                        print("FAIL", port,node["ip"], e)
            self.con_nodes.setdefault(node["ip"], {"connected": connected})

                        
            self.persist_data()        
            time.sleep(self.interval)

data_collector = DataCollector()
data_collector.fetch_data()
# collector_thread = Thread(target=data_collector.fetch_data, name="DataCollectorThread")
# collector_thread.start()
# print(collector_thread.name)
# collector_thread.join()


# Get all nodes, check if success, then connect. 