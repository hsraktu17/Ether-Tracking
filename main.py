from requests import get
from matplotlib import pyplot as plt
from datetime import datetime

API_KEY = "TPRJEXZ1A2STPSYEB442IDH9296U43A1K7"

address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"

''' https://api.etherscan.io/api
   ?module=account
   &action=balance
   &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   &tag=latest
   &apikey=YourApiKeyToken '''

# BASE_URL = "https://api.etherscan.io/api"


BASE_URL = "https://api.etherscan.io/api"
ETHER_VAl = 10 ** 18


def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


def get_account_balance(address):
    get_balance_url = make_api_url("account", "balance", address, tag="latest", x="2")

    response = get(get_balance_url)
    data = response.json()
    value = int(data["result"]) / ETHER_VAl

    return value


'''https://api.etherscan.io/api
   ?module=account
   &action=txlist
   &address=0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC
   &startblock=0
   &endblock=99999999
   &page=1
   &offset=10
   &sort=asc
   &apikey=YourApiKeyToken'''


def get_transaction(address):
    get_transaction_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1,
                                       offset=10000, sort="asc")
    response = get(get_transaction_url)
    data = response.json()["result"]

    current_balance = 0
    balances = []
    times = []


    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"])/ETHER_VAl
        gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VAl
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas

        balances.append(current_balance)
        times.append(time)
    plt.plot(times,balances)
    plt.show()

address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
get_transaction(address)
