import time
import requests

MSK_members = ["deadmonkey26", "plsnobanerino", "zak786786"]


def fetch_auction_data(weapon, session):
    url = f'https://api.warframe.market/v1/auctions/search?type=riven&buyout_policy=direct&weapon_url_name={weapon}&sort_by=price_asc'
    for retry in range(100):
        try:
            response = session.get(url, timeout=100)  # Wait for up to 10 seconds for a response
            data = response.json()
            auctions = [auction for auction in data['payload']['auctions'] if
                        auction['owner']['status'] == 'ingame' and not auction["owner"]["ingame_name"] in MSK_members]
            return auctions[0]['buyout_price'] if auctions else 0, weapon
        except (requests.exceptions.Timeout, KeyError, ValueError):
            # Handle cases where the request times out or the response is empty or not in the expected format
            time.sleep(1)  # Wait for 1 second before retrying
    return None, weapon
