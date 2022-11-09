string = "35.199.162.229"
print(len(string))

some = {"john":False}
if not "john" in some or some["john"] != False:
    print("YES")

if 1 and 0 or 1:
    print("yep")

some_dict = {}

some_dict.setdefault("node", {"connected": True})
print(some_dict)
print(some_dict["node"].get("success"))
# if some_dict["node"]["success"]:
#     some_dict["node"]["success"] = 1
# else:
    
some_dict["node"]["success"] = 1
print(some_dict)

connected_nodes = {"ip": {"connected": True, "john": False}}
if connected_nodes["ip"].get("connected") == True:
    print("EEEEE")
    

