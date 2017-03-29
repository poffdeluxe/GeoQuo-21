import sys
import os
import flask
import json

import datetime
import pytz

from two1.wallet import Wallet
from two1.bitserv.flask import Payment

app = flask.Flask(__name__)

# Setup 21.co
TWO1_WALLET_MNEMONIC = os.environ.get("TWO1_WALLET_MNEMONIC")
TWO1_USERNAME = os.environ.get("TWO1_USERNAME")

wallet = Wallet.import_from_mnemonic(mnemonic=TWO1_WALLET_MNEMONIC)
payment = Payment(app, wallet)

cities_by_name = {}


def load_cities():
    with open('data/cities.json') as cities_file:
        cities_data = json.load(cities_file)

    for city_key, city in cities_data.items():
        city_name = city['name']
        city['population'] = int(city['population'])

        city_array = cities_by_name.get(city_name, [])
        cities_by_name[city_name] = city_array + [city]


def city_matches(city, country_code=None, state=None):
    if country_code and city['countrycode'] != country_code:
        return False

    if country_code == 'US' and state and city['state'] != state:
        return False

    return True


def get_city(city_name, country_code=None, state=None):
    city_array = cities_by_name.get(city_name)

    if not city_array:
        return None

    # Filter out cities based on our filter params
    filtered_city_array = [c for c in city_array if city_matches(c, country_code=country_code, state=state)]

    if not filtered_city_array:
        # No matches
        return None

    if len(filtered_city_array) == 1:
        # We found just one!
        return filtered_city_array[0]

    # If more than one, choose based on population
    return max(filtered_city_array, key=lambda c: c['population'])


@app.route('/<city_name>')
@app.route('/<city_name>/<country_code>')
@app.route('/<city_name>/<country_code>/<state>')
#@payment.required(5000)
def get_city_time(city_name, country_code=None, state=None):
    city = get_city(city_name, country_code=country_code, state=state)

    if not city:
        # TODO: better error handler
        return 'Could not find city specified', 400

    # Filter out unneeded attributes
    city_attrs = ['timezone', 'name', 'countrycode', 'state']
    city_res = {k: v for k, v in city.items() if k in city_attrs}

    # Calc local time
    city_res['localtime'] = datetime.datetime.now(pytz.timezone(city['timezone'])).isoformat()

    return flask.jsonify(city_res)


if __name__ == "__main__":
    load_cities()

    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]

    app.run(host="::", port=port)
