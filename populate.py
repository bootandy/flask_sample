import requests
import json

with open('impressions-shortlist') as f:
    js = f.readline()
    count = 0
    failures = 0

    while js:
        rs = requests.post('http://localhost:5000/new_data', json = json.loads(js))
        if rs.status_code != requests.codes.ok:
            print(js)
            print('Error: '+str(rs.text))
            failures += 1
        js = f.readline()
        count +=1

print("data inserted attempted: %i failures: %i"%(count, failures))
