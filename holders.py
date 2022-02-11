import json
import argparse
import requests

SCOPE_URL = "https://api-cypress-v2.scope.klaytn.com/v2"
HOLDERS_URL = SCOPE_URL + "/tokens/{address}/holders"

session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "authroity": "api-cypress-v2.scope.klaytn.com",
        "origin": "https://scope.klaytn.com",
        "referrer": "https://scope.klaytn.com/",
    }
)


def get_nft_holders_by_address(address):
    url = HOLDERS_URL.format(address=address)
    holders = []
    page = 1
    while True:
        res = session.get(url, params={"page": page})
        parsed = json.loads(res.text)
        if not parsed.get("result"):
            break

        print(json.dumps(parsed.get("result"), indent=2))
        holders.extend(parsed.get("result"))
        page += 1

    return holders


def main(args):
    holders = get_nft_holders_by_address(args.address)

    with open("holders.json", "w") as f:
        json.dumps(holders, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        # default = doge sound club
        "--address",
        default="0xe47e90c58f8336a2f24bcd9bcb530e2e02e1e8ae",
    )
    args = parser.parse_args()

    main(args)
