from operator import itemgetter
import requests

def orders(item_link):
    base_url = "https://api.warframe.market/v1/items/"
    if " " in item_link:
        item_link = item_link.replace(" ", "_")
        url = f"{base_url}{item_link}/orders"
    else:
        item_link = f"{item_link}_prime_set"
        url = f"{base_url}{item_link}/orders"

    response = requests.get(url)
    raw = response.json()
    orders = raw['payload']['orders']

    orders_list: list = []
    for i in orders:
        orders_dict: dict = {'order_type': i['order_type'],
                             'platinum': i['platinum'],
                             'quantity': i['quantity'],
                             'reputation': i['user']['reputation'],
                             'avatar': i['user']['avatar'],
                             'ingame_name': i['user']['ingame_name'],
                             'status': i['user']['status'],
                             'creation_date': i['creation_date']}
        # print(orders_dict)
        if orders_dict['status'] == "ingame":
            orders_list.append(orders_dict)

    orders_list = sorted(orders_list, key=itemgetter('platinum'))
    buy_list: list = []
    sell_list: list = []

    for i in orders_list:
        if i['order_type'] == 'buy':
            buy_list.append(i)
        else:
            sell_list.append(i)

    orders_dict = {'buy': buy_list, 'sell': sell_list}
    return orders_dict