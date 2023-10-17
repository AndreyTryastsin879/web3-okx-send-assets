import random
import time

import pandas as pd

import okx.Funding as Funding

API_KEY = '8gb2d2f2-274b-455d-967e-9fdcb490f46c'
SECRET_KEY = 'D27A0AA2C55BC18B15055580921E56209'
PASSPHRASE = 'secret_phrase'

SETTINGS_XLSX = 'sending_settings_var_2.xlsx'
SETTINGS_TXT = 'sending_settings_var_2.txt'  # instead of loading excel
REPORT_NAME = 'report_table_var_2.xlsx'

MIN_TIMESLEEP_BETWEEN_TRANSACTIONS = 240
MAX_TIMESLEEP_BETWEEN_TRANSACTIONS = 480


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
assets_settings_for_sending = pd.read_excel(SETTINGS_XLSX)
list_of_assets_settings_for_sending = assets_settings_for_sending.to_dict('records')

# or load txt
# with open(SETTINGS_TXT, 'r') as file:
#     lines = file.readlines()
#
# list_of_assets_settings_for_sending = []
# for line in lines:
#     elements = line.strip().split(';')
#
#     wallet_address, asset_name, amount, fee, chain_name = elements[0].split(',')
#     data = {
#         'wallet_address': wallet_address,
#         'asset_name': asset_name,
#         'amount': amount,
#         'fee': fee,
#         'chain_name': chain_name
#     }
#
#     list_of_assets_settings_for_sending.append(data)

fundingAPI = Funding.FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

for row in list_of_assets_settings_for_sending:
    try:
        wallet_address, asset_name, amount, fee, chain = (row['wallet_address'], row['asset_name'],
                                                          row['amount'], row['fee'], row['chain'])

        print(f'Sending {amount} {asset_name} to address {wallet_address} in chain {chain}')

        api_response = fundingAPI.withdrawal(
            ccy=asset_name,
            toAddr=wallet_address,
            amt=amount - fee,
            fee=fee,
            dest="4",
            chain=chain
        )

        if api_response['code'] == '0':
            print('Sent')
            print('Creating report', '\n')
            report_table = open_table()
            create_report(report_table, wallet_address, asset_name, chain, amount, '-')

        elif api_response['code'] != '0':
            print('Didnt send')
            print('Creating report', '\n')
            error_code = api_response['code']
            error_message = api_response['msg']
            error_report_string = f'{error_code}-{error_message}'

            report_table = open_table()
            create_report(report_table, wallet_address, asset_name, chain, amount, error_report_string)

        time_sleep_value = random.choice(range(MIN_TIMESLEEP_BETWEEN_TRANSACTIONS,
                                               MAX_TIMESLEEP_BETWEEN_TRANSACTIONS))
        print('Delay', time_sleep_value, '\n')

        time.sleep(time_sleep_value)

    except Exception as error:
        print('Didnt send')
        print('Creating report', '\n')
        report_table = open_table()
        create_report(report_table, '-', '-', '-', '-', error)