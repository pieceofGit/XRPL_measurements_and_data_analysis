from threading import Thread
import json
import requests
import time
"""Currently a prototype storing data in json and only requesting data from one node"""
class DataCollector:
    """Periodically requests data about all nodes on XRPL nodes and stores in database"""
    def __init__(self, interval=60*15) -> None:
        self.nodes = [{"host":"r.ripple.com", "port":"51234/"}]
        self.interval = interval
        with open("node_measurements.json", "r") as f:
            self.data = json.load(f)
        self.server_info_req = json.dumps({"method": "server_info", "params": [{}]})
    
    def persist_data(self) -> None:
        """Persists data in json file"""
        try:
            with open("node_measurements.json", "w+") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print("Could not store data: ", e)
    
    def fetch_data(self) -> None:
        """Periodically fetches data from nodes based on interval"""
        while True:
            for node in self.nodes: 
                try:
                    response = requests.get("https://"+node["host"]+":"+node["port"], timeout=2, verify=False, data=self.server_info_req).json()
                    self.data.setdefault(node["host"], []).append(response["result"])
                except Exception as e:
                    print("Could not fetch data: ", e)
            self.persist_data()        
            time.sleep(self.interval)

data_collector = DataCollector(2)
# data_collector.fetch_data()
collector_thread = Thread(target=data_collector.fetch_data, name="DataCollectorThread")
collector_thread.start()
print(collector_thread.name)
collector_thread.join()

