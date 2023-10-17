# web3-okx-send-assets

RU

Простые скрипты для вывода крипты с биржи okx на кошельки и скрипты, чтобы отправить крипту с кошельков на саб-аккаунты биржи

Подробное описание кода можно прочитать на сайте:
https://crypto-py.com/14-cex/83-otpravka-kripty-s-okx-na-koshelki-po-api-otpravka-kripty-s-koshelkov-na-sabakkauty-na-python-web3

Или в файле .ipynb в репозитории.

withdraw-from-okx-to-wallets-var-1.py - для отправки одного вида монет в равном количестве на кошельки. В этом скрипте используются файлы:
Список адресов получателей в excel wallet_addresses_var_1.xlsx или txt - wallet_addresses_var_1.txt.
Результат работы скрипта записывается в отчет excel - report_table_var_1.xlsx.

withdraw-from-okx-to-wallets-var-2.py - настраиваемая отправка: разные монеты в разном количестве на кошельки. В этом скрипте используются файлы:
Настройки для отправки (адрес, название монеты, количество, комиссия, сеть) в формате excel sending_settings_var_2.xlsx или txt - sending_settings_var_2.txt.
Результат работы скрипта записывается в отчет excel - report_table_var_2.xlsx.

withdraw-from-wallets-to-okx-var-1.py - отправка нативных монет с кошельков на саб-аккаунты биржи. В этом скрипте используются файлы:
Настройки для отправки (приватный ключ кошелька, адрес okx, название монеты, название сети, количество, url rpc) в формате excel sending_from_wallets_settings_var_1.xlsx или txt - sending_from_wallets_settings_var_1.txt.
Результат работы скрипта записывается в отчет excel - report_table_var_sending_from_wallets_1.xlsx.

withdraw-from-wallets-to-okx-var-2.py - отправка токенов, например стейблов с кошельков на саб-аккаунты биржи. В этом скрипте используются файлы:
Настройки для отправки (приватный ключ кошелька, адрес okx, название монеты, название сети, адрес смарт-контракта, количество, url rpc) в формате excel sending_from_wallets_settings_var_2.xlsx или txt - sending_from_wallets_settings_var_2.txt.
ABI для работы отправки ERC20 токенов в формате json ERC20_ABI.json.
Результат работы скрипта записывается в отчет excel - report_table_var_sending_from_wallets_2.xlsx.

Также 2 дополнительных скрипта:
get-assets-info.py - скрипт для получения информации о монетах, которые в okx: название, название сети, минимальная и максимальная комиссия. Результат экспортируется в assets_settings.xlsx.
count-withdrawal-cost-from-okx.py - скрипт для предварительного расчета необходимой суммы на балансе с учетом комиссий, чтобы осуществить отправку в скрипте withdraw-from-okx-to-wallets-var-1.py.

========================================================================
EN

Simple scripts to withdraw crypto from the OKX exchange to wallets, and scripts to send crypto from wallets to the exchange’s sub-accounts.

You can find a detailed description of the code on the website:

https://crypto-py.com/14-cex/83-otpravka-kripty-s-okx-na-koshelki-po-api-otpravka-kripty-s-koshelkov-na-sabakkauty-na-python-web3

Or in the .ipynb file in the repository.

withdraw-from-okx-to-wallets-var-1.py: For sending one type of coin in equal quantities to wallets. This script uses the following files:
List of recipient addresses in Excel wallet_addresses_var_1.xlsx or TXT wallet_addresses_var_1.txt.
The script's output is saved in an Excel report, report_table_var_1.xlsx.

withdraw-from-okx-to-wallets-var-2.py: Customizable sending of different coins in different quantities to wallets. This script uses the following files:
Sending settings (address, coin name, quantity, fee, network) in Excel format, sending_settings_var_2.xlsx or TXT sending_settings_var_2.txt.
The script's output is saved in an Excel report, report_table_var_2.xlsx.

withdraw-from-wallets-to-okx-var-1.py: Sending native coins from wallets to the exchange's sub-accounts. This script uses the following files:
Sending settings (wallet private key, OKX address, coin name, network name, quantity, RPC URL) in Excel format, sending_from_wallets_settings_var_1.xlsx or TXT sending_from_wallets_settings_var_1.txt.
The script's output is saved in an Excel report, report_table_var_sending_from_wallets_1.xlsx.

withdraw-from-wallets-to-okx-var-2.py: Sending tokens, such as stablecoins, from wallets to the exchange's sub-accounts. This script uses the following files:
Sending settings (wallet private key, OKX address, coin name, network name, smart contract address, quantity, RPC URL) in Excel format, sending_from_wallets_settings_var_2.xlsx or TXT sending_from_wallets_settings_var_2.txt.
ABI for working with ERC20 tokens in JSON format, ERC20_ABI.json.
The script's output is saved in an Excel report, report_table_var_sending_from_wallets_2.xlsx.


Additionally, there are two additional scripts:

get-assets-info.py: A script for obtaining information about coins on OKX, including name, network name, minimum and maximum fees. The results are exported to assets_settings.xlsx.

count-withdrawal-cost-from-okx.py: A script for a preliminary calculation of the required balance, considering fees, to perform withdrawals in the withdraw-from-okx-to-wallets-var-1.py script.
