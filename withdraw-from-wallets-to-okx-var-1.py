import random
import time

from web3 import Web3

import pandas as pd

SETTINGS_XLSX = 'sending_from_wallets_settings_var_1.xlsx'
SETTINGS_TXT = 'sending_from_wallets_settings_var_1.txt'  # instead of loading excel

MIN_TIMESLEEP_BETWEEN_TRANSACTIONS = 240
MAX_TIMESLEEP_BETWEEN_TRANSACTIONS = 480

REPORT_NAME = 'report_table_var_sending_from_wallets_1.xlsx'


def excel_export(table, table_name):
    writer_kernel = pd.ExcelWriter(table_name, engine='xlsxwriter')
    table.to_excel(writer_kernel, index=False)
    writer_kernel.close()


def open_table():
    try:
        table = pd.read_excel(REPORT_NAME)

        return table.to_dict('records')

    except:
        table_template = pd.DataFrame(index=[0])
        excel_export(table_template, REPORT_NAME)
        created_table = pd.read_excel(REPORT_NAME)

        return created_table.to_dict('records')


def create_report(report_table, wallet_address, okx_address,
                  asset_name, chain, sent_amount, txn_hash, error):
    report_dict = dict()
    report_dict['wallet_address'] = wallet_address
    report_dict['okx_address'] = okx_address
    report_dict['asset_name'] = asset_name
    report_dict['chain'] = chain
    report_dict['sent_amount'] = sent_amount
    report_dict['txn_hash'] = txn_hash
    report_dict['error'] = error

    report_table.append(report_dict)
    result_table = pd.DataFrame.from_dict(report_table)
    result_table.dropna(inplace=True)
    excel_export(result_table, REPORT_NAME)


# load excel
settings_for_sending_from_wallets = pd.read_excel(SETTINGS_XLSX)
list_of_settings_for_sending_from_wallets = settings_for_sending_from_wallets.to_dict('records')

# or load txt
# with open(SETTINGS_TXT, 'r') as file:
#     lines = file.readlines()
#
# list_of_assets_settings_for_sending = []
# for line in lines:
#     elements = line.strip().split(';')
#
#     private_key, okx_sub_address, asset_name, chain_name, amount, chain_rpc = elements[0].split(',')
#     data = {
#         'private_key': private_key,
#         'okx_sub_address': okx_sub_address,
#         'asset_name': asset_name,
#         'chain_name': chain_name,
#         'amount': amount,
#         'chain_rpc': chain_rpc
#     }
#
#     list_of_assets_settings_for_sending.append(data)

for row in list_of_settings_for_sending_from_wallets:
    try:
        private_key, okx_sub_address, asset_name, chain_name, amount, chain_rpc = (row['private_key'],
                                                                                   row['okx_sub_address'],
                                                                                   row['asset_name'],
                                                                                   row['chain_name'],
                                                                                   row['amount'],
                                                                                   row['chain_rpc'])

        web3 = Web3(Web3.HTTPProvider(chain_rpc))

        from_address = web3.eth.account.from_key(private_key).address

        print(f'Sending {amount} {asset_name} on the {chain_name} network from address {from_address}')

        to_address = web3.to_checksum_address(okx_sub_address)

        print(f'To OKX address {to_address}')

        amount_wei = int(web3.to_wei(amount, 'ether'))

        gas_price = web3.eth.gas_price

        estimated_gas = web3.eth.estimate_gas({
            'to': to_address,
            'value': amount_wei,
        })

        fee = gas_price * estimated_gas

        nonce = web3.eth.get_transaction_count(from_address)

        transaction_settings = {
            'chainId': web3.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': amount_wei - fee,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': estimated_gas,
        }

        sent_amount = float(web3.from_wei(amount_wei - fee, 'ether'))

        signed_transaction = web3.eth.account.sign_transaction(transaction_settings, private_key)

        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        print('Sent')
        print('Txn hash:', transaction_hash.hex())

        print('Creating report')
        report_table = open_table()
        create_report(report_table, from_address, to_address,
                      asset_name, chain_name, sent_amount, transaction_hash.hex(), '-')

        time_sleep_value = random.choice(range(MIN_TIMESLEEP_BETWEEN_TRANSACTIONS,
                                               MAX_TIMESLEEP_BETWEEN_TRANSACTIONS))
        print('Delay', time_sleep_value, '\n')

        time.sleep(time_sleep_value)

    except Exception as error:
        print('Didnt send')
        print('Creating report')
        report_table = open_table()
        create_report(report_table, from_address, to_address,
                      asset_name, chain_name, '-', '-', error)

