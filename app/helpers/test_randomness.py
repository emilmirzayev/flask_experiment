import requests
from collections import Counter
import argparse

url = "http://127.0.0.1:5000/events/"
data = {"event_type":1}

parser = argparse.ArgumentParser()

parser.add_argument("-n", type = int, help = "number of iterations to run", default = 100)
parser.add_argument("-p", type = bool, help = "print the resulting sequence", default = False)
args = parser.parse_args()


stats = []
for i in range(args.n):
    

    response = requests.post(url= url,
                       json = data
    )

    stats.append(response.json()["treatment_group"])

if args.p:
    print(stats)

print(Counter(stats))