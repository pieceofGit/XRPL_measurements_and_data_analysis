ports = ["33", "333", "3332"]
node = {"port": "444"}
the_ports = ports
the_ports.append(node["port"])
print(ports)

dict = {"john": "5"}
print(dict.get("steve", 5))
ports = ["3", "33"]
for port in ports:
    print("YES")
    ports = []