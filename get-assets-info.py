import pandas as pd

import okx.Funding as Funding

API_KEY = '8gb2d2f2-274b-455d-967e-9fdcb490f46c'
SECRET_KEY = 'D27A0AA2C55BC18B15055580921E56209'
PASSPHRASE = 'secret_phrase'

fundingAPI = Funding.FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

result = fundingAPI.get_currencies()

list_of_dicts = []
for element in range(len(result['data'])):
    dictionary = dict()
    dictionary['asset_name'] = result['data'][element]['ccy']
    dictionary['chain_name'] = result['data'][element]['chain']
    dictionary['min_fee'] = result['data'][element]['minFee']
    dictionary['max_fee'] = result['data'][element]['maxFee']
    list_of_dicts.append(dictionary)

df = pd.DataFrame.from_dict(list_of_dicts)

writer_kernel = pd.ExcelWriter('assets_settings.xlsx', engine='xlsxwriter')
df.to_excel(writer_kernel, index=False)
writer_kernel.close()