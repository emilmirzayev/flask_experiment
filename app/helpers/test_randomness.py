import requests
from collections import Counter
url = "http://127.0.0.1:5000/events/"
data = {"event_type":1}

stats = []
for i in range(30):
    

    response = requests.post(url= url,
                       json = data
    )

    stats.append(response.json()["treatment_group"])


print(Counter(stats))