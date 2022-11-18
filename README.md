# Xrpl_Data_Gathering
 
A data gathering and analyzing project on the XRP Ledger.

## Data Collector
Gets list of nodes on the network through /crawl endpoint of XRPL node.
See: https://xrpl.org/peer-crawler.html
Attempts to fetch data about "server_state" from each node on the network through an HTTP or websocket request.
See: https://xrpl.org/server_state.html
The data collector currently stores all successful requests in node_measurements.json and a separate logging of connected nodes stored in connected_nodes.json.

## Data Analyzer
Analyzes the data from the node_measurements file. Currently very barebones. 
