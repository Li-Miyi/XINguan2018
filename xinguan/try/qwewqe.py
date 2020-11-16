import requests
import json
req = requests.get("http://api.map.baidu.com/geocoding/v3/?address=四川省成都市四川大学望江校区&output=json&ak=ZtiExca5mcvFwBEfTL3B8eVg7ATjZb2f&callback=showLocation")
dic = json.loads(req.text.replace("showLocation&&showLocation(","").replace("(","").replace(")",""))

print(dic)
