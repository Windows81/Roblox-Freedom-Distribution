import json
import requests
import re
j = json.load(open('MaterialPacks.json', 'r'))

d = {}
for pn, p in j.items():
    r = {}
    for mn, m in p.items():
        t = ''.join(
            requests.get(
                f'https://assetdelivery.roblox.com/v1/asset/?id={i}').text
            for i in m['ids']
        )
        r[mn] = dict(re.findall(r'<([a-z]+)>([0-9]+)', t))
    d[pn] = r
    print(r)

json.dump(d, open('MaterialPacks2.json', 'w'))

r = []
for pn, p in d.items():
    for mn, m in p.items():
        for tn, t in m.items():
            r.append(f"'rbx-mtl-{mn}-{tn}.dds': {t}")
    r.append('\n')
