import requests
import json
from fetch_auction_data import fetch_auction_data, MSK_members

#
def Signin():
    with open("wfm.txt", "r") as f:
        lines = f.read().splitlines()
        email = lines[0]
        password = lines[1]
    # email = input("Enter your email: ")
    # password = input("Enter your password: ")

    # Set up the URL and data for the sign-in request
    url = 'https://api.warframe.market/v1/auth/signin'
    data = {"auth_type": 'header', 'email': email, 'password': password}
    headers = {
        "Authorization": "JWT",
        "language": "en",
        "accept": "application/json",
        "platform": "pc",
        "auth_type": "header"}

    # Make the sign-in request and store the response
    response = requests.post(url, json=data, headers=headers)
    jwt = response.headers["Authorization"]
    username = response.json()["payload"]["user"]["ingame_name"]
    # print(json.dumps(response.json(), indent=1))
    return response, username, jwt


def GetRivenAuctions():
    # Make the request and store the response
    response = requests.get(f'https://api.warframe.market/v1/profile/{username}/auctions')
    return response


def GetOrders():
    response = requests.get(f'https://api.warframe.market/v1/profile/{username}/orders')
    return response


def FetchOrderData(item_name, mod_rank):
    response = requests.get(f'https://api.warframe.market/v1/items/{item_name}/orders')
    # print(json.dumps(response.json(), indent=1))
    if mod_rank > 0:
        sell_orders = [sell_order for sell_order in response.json()["payload"]["orders"] if
                       sell_order["order_type"] == "sell" and sell_order["user"]["status"] == 'ingame'
                       and not sell_order["user"]["ingame_name"] in MSK_members and sell_order["mod_rank"] == mod_rank]

    else:
        sell_orders = [sell_order for sell_order in response.json()["payload"]["orders"] if
                       sell_order["order_type"] == "sell" and sell_order["user"]["status"] == 'ingame'
                       and not sell_order["user"]["ingame_name"] in MSK_members]

    # print(json.dumps(sell_orders, indent=1))
    sorted_sell_orders = sorted(sell_orders, key=lambda x: x['platinum'])
    # print(json.dumps(sorted_sell_orders, indent=1))
    return sorted_sell_orders[0]["platinum"]


def UpdateOrders(price, order_id):
    url = f'https://api.warframe.market/v1/profile/orders/{order_id}'

    data = {
        "order_id": f"{order_id}",
        "platinum": price,
        "visible": "true"
    }

    headers = {
        "Authorization": jwt,
        "language": "en",
        "accept": "application/json",
        "platform": "pc",
        "auth_type": "header"}

    response = requests.put(url, json=data, headers=headers)
    return response


def UpdateRivenAuction(price, auction_id):
    url = f'https://api.warframe.market/v1/auctions/entry/{auction_id}'

    data = {
        "order_id": f"{auction_id}",
        "buyout_price": price,
        "starting_price": price,
        "visible": "true"
    }
    headers = {
        "Authorization": jwt,
        "language": "en",
        "accept": "application/json",
        "platform": "pc",
        "auth_type": "header"}

    response = requests.put(url, json=data, headers=headers)
    return response


while True:
    response, username, jwt = Signin()

    # Check if the sign-in was successful
    if response.ok:
        pass
    else:
        print(f'Sign-in failed with error: {response.json()["error"]}')
        break

    response = GetOrders()

    # Check if the GetOrders was successful
    if response.ok:
        # Extract your sell order listings from the response
        orders = response.json()['payload']['sell_orders']

        # Print the order listings
        print(f"You have {len(orders)} orders:")
        # print(json.dumps(response.json(), indent=1))

        for order in orders:
            print(f"- {order['item']['url_name']} (id: {order['id']}, price: {order['platinum']} platinum)")
            try:
                mod_rank = order['mod_rank']
            except KeyError:
                mod_rank = 0
            new_price = FetchOrderData(order['item']['url_name'], mod_rank)
            item_id = order['id']
            print(new_price)

            if new_price != order['platinum'] - 1:
                response = UpdateOrders(new_price - 1, item_id)

                # Check if the UpdateOrders was successful
                if response.ok:
                    # Print the order details
                    # print(json.dumps(response.json(), indent=1))
                    order_data = json.loads(response.text)["payload"]["order"]
                    print(f"Order updated! name: {order_data['item']['url_name']} price: {order_data['platinum']}")
                else:
                    print(f'Error updating orders: {response.json()["error"]}')
                    break
            else:
                print("Already cheapest order")
    else:
        print(f'GetOrder request failed with error: {response.json()["error"]}')
        break

    response = GetRivenAuctions()

    # Check if the GetRivenAuctions was successful
    if response.ok:
        # Extract your auction listings from the response
        auctions = [auction for auction in response.json()['payload']['auctions'] if auction["item"]["mod_rank"] == 0]

        # Print the auction listings
        print(f"You have {len(auctions)} auctions:")
        # print(json.dumps(response.json(), indent=1))
        for auction in auctions:
            lowest_weapon_price = fetch_auction_data(auction['item']['weapon_url_name'], requests)
            new_price = lowest_weapon_price[0]
            weapon_id = auction['id']
            # weapon_data =
            print(new_price)
            print(
                f"- {auction['item']['weapon_url_name']} {auction['item']['name']} (id: {auction['id']}, price: {auction['buyout_price']} platinum)")
            # print(json.dumps(auction, indent=1))

            if new_price != auction['buyout_price'] - 1:
                response = UpdateRivenAuction(new_price - 1, weapon_id)

                # Check if the UpdateRivenAuctions was successful
                if response.ok:
                    # Print the auction details
                    # print(json.dumps(response.json(), indent=1))
                    auction_data = json.loads(response.text)["payload"]["auction"]
                    print(
                        f"Auction updated! name: {auction_data['item']['weapon_url_name']} {auction_data['item']['name']}, price: {auction_data['buyout_price']}")
                else:
                    print(f'Error updating auction: {response.json()["error"]}')
            else:
                print("Already cheapest auction")
    else:
        print(f'GetRivenAuctions failed with error: {response.json()["error"]}')
        break
    break
