import requests
import random

if __name__ == "__main__":
    p = {'x':random.randrange(1,10000000)}
    r = requests.get('http://localhost:5000/test', params = p)
    print(r.json())
    gto = r.json()['goto']
    r2 = requests.get(f"http://localhost:5000/test/result/{gto}")
    print(r2.json())