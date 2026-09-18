import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_customers():
    return load_json("customers.json")


def get_bookings():
    return load_json("bookings.json")


def get_policies():
    return load_json("policies.json")


def get_customer(pnr):
    customers = get_customers()

    for customer in customers:
        if customer["booking_reference"].lower() == pnr.lower():
            return customer

    return None


def get_customer_booking(pnr):
    bookings = get_bookings()

    return [
        booking
        for booking in bookings
        if booking["pnr"].lower() == pnr.lower()
    ]