import random
import time

import pandas as pd

import okx.Funding as Funding

API_KEY = '8gb2d2f2-274b-455d-967e-9fdcb490f46c'
SECRET_KEY = 'D27A0AA2C55BC18B15055580921E56209'
PASSPHRASE = 'secret_phrase'

SETTINGS_XLSX = 'wallet_addresses_var_1.xlsx'
SETTINGS_TXT = 'wallet_addresses_var_1.txt'  # instead of loading excel

ASSET_NAME = 'USDC'
CHAIN_NAME = 'USDC-Arbitrum One (Bridged)'
FEE = 0.1
TOTAL_SENDING_AMOUNT = 10

MIN_TIMESLEEP_BETWEEN_TRANSACTIONS = 240
MAX_TIMESLEEP_BETWEEN_TRANSACTIONS = 480

MIN_VALUE_IN_RANGE_DIVIDER = 10000
MAX_VALUE_IN_RANGE_DIVIDER = 100

REPORT_NAME = 'report_table_var_1.xlsx'


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


def create_report(report_table, address, asset_name, chain, sent_amount, error):
    report_dict = dict()
    report_dict['address'] = address
    report_dict['asset_name'] = asset_name
    report_dict['chain'] = chain
    report_dict['sent_amount'] = sent_amount
    report_dict['error'] = error

    report_table.append(report_dict)

    result_table = pd.DataFrame.from_dict(report_table)

    result_table.dropna(inplace=True)

    excel_export(result_table, REPORT_NAME)


# load excel
wallet_addresses_xlsx = pd.read_excel(SETTINGS_XLSX)
wallet_addresses_list = wallet_addresses_xlsx['address'].to_list()

# or load txt
with open(SETTINGS_TXT, 'r') as f:
    data = f.readlines()
    wallet_addresses_list = [adress.replace('\n', '') for adress in data]

fundingAPI = Funding.FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

for address in wallet_addresses_list:
    try:
        sending_amount = (TOTAL_SENDING_AMOUNT / len(wallet_addresses_list) -
                          FEE -
                          random.uniform(TOTAL_SENDING_AMOUNT / MIN_VALUE_IN_RANGE_DIVIDER,
                                         TOTAL_SENDING_AMOUNT / MAX_VALUE_IN_RANGE_DIVIDER))

        print(f'Sending {sending_amount} {ASSET_NAME} to address {address} in chain {CHAIN_NAME}')

        api_response = fundingAPI.withdrawal(
            ccy=ASSET_NAME,
            toAddr=address,
            amt=sending_amount,
            fee=FEE,
            dest="4",
            chain=CHAIN_NAME
        )

        if api_response['code'] == '0':
            print('Sent')
            print('Creating report', '\n')
            report_table = open_table()
            create_report(report_table, address, ASSET_NAME, CHAIN_NAME, sending_amount, '-')

        elif api_response['code'] != '0':
            print('Didnt send')
            print('Creating report', '\n')
            error_code = api_response['code']
            error_message = api_response['msg']
            error_report_string = f'{error_code}-{error_message}'

            report_table = open_table()
            create_report(report_table, address, ASSET_NAME, CHAIN_NAME, sending_amount, error_report_string)

        time_sleep_value = random.choice(range(MIN_TIMESLEEP_BETWEEN_TRANSACTIONS,
                                               MAX_TIMESLEEP_BETWEEN_TRANSACTIONS))
        print('Delay', time_sleep_value, '\n')

        time.sleep(time_sleep_value)

    except Exception as error:
        print('Didnt send')
        print('Creating report', '\n')
        report_table = open_table()
        create_report(report_table, '-', '-', '-', '-', error)

