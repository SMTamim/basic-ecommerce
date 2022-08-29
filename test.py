from pprint import pprint as pp

import requests

data = {
    'count': 10,
    'page': 1
}
res = requests.post('http://127.0.0.1:5000/api/products', json=data)
pp(res.json())
