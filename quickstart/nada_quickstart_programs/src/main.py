from nada_dsl import *

def initialize_parties(nr_producers, nr_consumers):
    producers = [Party(name=f"Producer{i}") for i in range(nr_producers)]
    consumers = [Party(name=f"Consumer{i}") for i in range(nr_consumers)]
    return producers, consumers

def inputs_initialization(producers, consumers):
    energy_offers = []
    for p in producers:
        offer_quantity = SecretUnsignedInteger(Input(name=f"offer_quantity_{p.name}", party=p))
        offer_price = SecretUnsignedInteger(Input(name=f"offer_price_{p.name}", party=p))
        energy_offers.append((offer_quantity, offer_price))
    
    energy_bids = []
    for c in consumers:
        bid_quantity = SecretUnsignedInteger(Input(name=f"bid_quantity_{c.name}", party=c))
        bid_price = SecretUnsignedInteger(Input(name=f"bid_price_{c.name}", party=c))
        energy_bids.append((bid_quantity, bid_price))
    
    return energy_offers, energy_bids

def match_trades(energy_offers, energy_bids):
    matches = []
    for bid_quantity, bid_price in energy_bids:
        best_offer = None
        for offer_quantity, offer_price in energy_offers:
            if offer_price <= bid_price and (best_offer is None or offer_price < best_offer[1]):
                best_offer = (offer_quantity, offer_price)
        if best_offer:
            matches.append((bid_quantity, best_offer[0], best_offer[1]))
    return matches

def calculate_final_payments(matches):
    final_payments = []
    for bid_quantity, offer_quantity, offer_price in matches:
        trade_quantity = bid_quantity if (bid_quantity < offer_quantity) else offer_quantity
        final_payment = trade_quantity * offer_price
        final_payments.append(final_payment)
    return final_payments

def nada_main():
    nr_producers = 5
    nr_consumers = 5
    outparty = Party(name="OutParty")

    producers, consumers = initialize_parties(nr_producers, nr_consumers)
    energy_offers, energy_bids = inputs_initialization(producers, consumers)

    matches = match_trades(energy_offers, energy_bids)
    final_payments = calculate_final_payments(matches)

    # Create Output objects for each final payment
    output_payments = [Output(final_payment, name=f"final_payment_{i}", party=outparty) for i, final_payment in enumerate(final_payments)]

    return output_payments

