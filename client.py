import os
from time import sleep

import requests
from requests.models import Response

while True:
    response: Response = requests.get(os.environ["PROXY_URL"])
    print(response.json())
    sleep(float(os.getenv("SLEEP_TIME", 0)))
