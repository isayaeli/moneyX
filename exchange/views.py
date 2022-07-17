from django.shortcuts import render
import json
# from web3 import Web3

# url  = 'HTTP://127.0.0.1:7545'

# web3 = Web3(Web3.HTTPProvider(url))

# account1 = '0x86Bb7Db5491C4797423d77FE32254D5bFbF419C9'
# account2 = '0x36746C8d9839ADA1fDEfB5C4b332ae3EA77Ad906'

# private_key = 'cfc0f2b6e5967a0c2ae17342a1f5e065e87c57c56ccf0de7bbd55e062ac82ada'

# nonce = web3.eth.getTransactionCount(account1)

# tx = {
#     'nonce': nonce,
#     'to':account2,
#     'value': web3.toWei(1, 'ether'),
#     'gas': 2000000,
#     "gasPrice":web3.toWei('50', 'gwei')
# }

# signed_tx =  web3.eth.account.signTransaction(tx, private_key)
# tx_hash =  web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# Create your views here.
def exchanging(request):

    if request.method == 'POST':
        # print(tx_hash)
        from_ =request.POST['from_']
        to = request.POST['to']
        amount_from = request.POST['amount_from']
        amount_to = request.POST['amount_to']

        context ={
            'amount_from':amount_from,
            'amount_to':amount_to,
            'to':to,
            'from_':from_
        }
    return render(request, 'exchange/exchanging.html', context)