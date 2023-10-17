import random

FEE = 0.1
TOTAL_SENDING_AMOUNT = 10

MIN_VALUE_IN_RANGE_DIVIDER = 10000
MAX_VALUE_IN_RANGE_DIVIDER = 100

WALLETS_QUANTITY = 10

total = []
for number in range(10):
    sent_amount = TOTAL_SENDING_AMOUNT / WALLETS_QUANTITY - FEE - random.uniform(
        TOTAL_SENDING_AMOUNT / MIN_VALUE_IN_RANGE_DIVIDER,
        TOTAL_SENDING_AMOUNT / MAX_VALUE_IN_RANGE_DIVIDER
    )

    print('Wallet №:', number, 'sent:', sent_amount)

    total.append(sent_amount)

print('Total amount sent:', sum(total), 'Total amount fee spent', FEE * WALLETS_QUANTITY)