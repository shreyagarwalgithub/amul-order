from croniter import croniter
import time
import yaml
import requests
from dataclasses import dataclass
import argparse

CONFIG_PATH = 'config.yaml'

@dataclass
class Credentials:
    mobile: str
    password: str | None = None

@dataclass
class Address:
    line1: str
    line2: str
    city: str
    state: str
    pincode: str

@dataclass
class CardInfo:
    number: str
    expiry: str
    cvv: str

@dataclass
class Config:
    credentials: Credentials
    address: Address
    card: CardInfo
    sku_url: str
    cron: str = '0 9 * * MON'

    @staticmethod
    def from_dict(data: dict) -> 'Config':
        creds = Credentials(**data['credentials'])
        addr = Address(**data['address'])
        card = CardInfo(**data['card'])
        cron = data.get('schedule', {}).get('cron', '0 9 * * MON')
        return Config(credentials=creds, address=addr, card=card, sku_url=data['sku_url'], cron=cron)


def load_config() -> Config:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return Config.from_dict(data)


def login(session: requests.Session, creds: Credentials) -> bool:
    """Attempt login using mobile credentials. Placeholder for actual API."""
    payload = {'mobile': creds.mobile}
    if creds.password:
        payload['password'] = creds.password
    resp = session.post('https://shop.amul.com/api/login', json=payload)
    return resp.ok


def add_to_cart(session: requests.Session, sku_url: str) -> bool:
    """Add the SKU to the cart. Placeholder for actual API call."""
    resp = session.post('https://shop.amul.com/api/cart/add', json={'sku_url': sku_url, 'qty': 1})
    return resp.ok


def checkout(session: requests.Session, address: Address, card: CardInfo) -> bool:
    """Perform checkout with saved address and card info. Placeholder for actual API."""
    data = {
        'address': address.__dict__,
        'card': card.__dict__,
    }
    resp = session.post('https://shop.amul.com/api/checkout', json=data)
    return resp.ok


def process_order():
    config = load_config()
    session = requests.Session()
    if not login(session, config.credentials):
        print('Login failed')
        return
    if not add_to_cart(session, config.sku_url):
        print('Add to cart failed')
        return
    if not checkout(session, config.address, config.card):
        print('Checkout failed')
        return
    print('Order placed successfully')



import datetime


def run_scheduler(config: Config) -> None:
    base = datetime.datetime.now()
    cron = croniter(config.cron, base)
    next_run = cron.get_next(datetime.datetime)
    print(f"Scheduler started with cron: {config.cron}")
    while True:
        now = datetime.datetime.now()
        if now >= next_run:
            process_order()
            next_run = cron.get_next(datetime.datetime)
        time.sleep(30)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Amul order automation")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the order flow once immediately and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    if args.once:
        process_order()
    else:
        run_scheduler(config)


if __name__ == "__main__":
    main()
