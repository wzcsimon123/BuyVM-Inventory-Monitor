'''
cron: */10 * * * * buyvm.py
new Env('buyvm库存监控');
'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import notify
import re

url = "https://my.frantech.ca/cart.php?gid=39" #修改此项更改区域

product_id = [i for i in range(1, 12)] #修改此项修改监控的机型 从1-11对应512MB - 32GB

tehran_timezone = pytz.timezone('Asia/Tehran')
tehran_time = datetime.now(tehran_timezone)
formatted_time = tehran_time.strftime('%Y-%m-%d %H:%M:%S')

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

for id in product_id:
    package_div = soup.find('div', {'class': 'package', 'id': 'product' + str(id)})
    qty_div = package_div.find('div', {'class': 'package-qty'})
    name_h3 = package_div.find('h3', {'class': 'package-name'})

    try:
        availability = qty_div.get_text(strip=True)
    except AttributeError:
        availability = "Unlimited"
    try:
        name = name_h3.get_text(strip=True)
    except AttributeError:
        name = "undefined"

    numbers = re.findall(r'-?\d+', availability)
    numbers = int(numbers[0])
    if numbers <= 0:
        msg = "Was not avalable"
        print(msg)
    else:
        msg = f"VPS {name} was Available at {formatted_time} and {numbers} vps were available"
        data = {"content": f"{msg}"}
        notify.send(f"vps {name} available", data["content"])
