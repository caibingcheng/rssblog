import json
import requests
fetch_list = {
    "bbing": "https://gist.githubusercontent.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3/raw/friends.json",
    "addition": "https://gist.githubusercontent.com/caibingcheng/adf8f300dc50a61a965bdcc6ef0aecb3/raw/addition.json"
}


rss = []
for (key, link) in fetch_list.items():
    rss_list = []
    try:
        rss_list = json.loads(requests.get(link).text)
    except:
        pass
    for rss_s in rss_list:
        rss_s['id'] = key
        rss.append(rss_s)
