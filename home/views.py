from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from home.models import Block, Transaction, Mempool, Blockchain, Miner, Wallet
from core.utils import (
    create_pending_transaction,
    validate_mining_request,
    create_or_get_blockchain,
    mine_transactions_to_block,
    build_blockchain_list,
    get_mempool_transactions
)

# Global storage for blockchain visualization
chain_list = {}


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def wallet(request):
    if request.method == 'POST':
        print(request.POST)
        mempool = Mempool.objects.filter(user_name=request.POST['miner'])[0]
        pending_transaction = create_pending_transaction(
            sender=request.user,
            receiver=request.POST['recieve'],
            amount=request.POST['amount'],
            mempool=mempool
        )
        
    if (len(Miner.objects.filter()) > 5):
        miners = Miner.objects.filter()[0:4]
    else:
        miners = Miner.objects.filter()[0:]
    my_dict = {'miners': miners}
    return render(request, 'wallet.html', context=my_dict)


@login_required
def mining_block(request):
    if request.method == 'POST':
        if not validate_mining_request(request.POST):
            return redirect('mining')
            
        blockchain, is_new = create_or_get_blockchain(request.user)
        
        # Extract selected transaction IDs from POST data
        selected_transaction_ids = []
        for key in request.POST.keys():
            if key[-3:] == 'box':
                selected_transaction_ids.append(key[0:-3])
        
        # Mine transactions into new block
        new_block = mine_transactions_to_block(blockchain, selected_transaction_ids)
        
        # Build blockchain visualization data
        global chain_list
        chain_list = build_blockchain_list(blockchain)
        
        return redirect('/mined')


@login_required
def mine(request):
    try:
        miner = Miner.objects.get(user=request.user.username)
    except Miner.DoesNotExist:
        return render(request, 'mine.html')
    return redirect('mining')


@login_required
def mining(request):
    if request.method == 'POST':
        if (request.POST.get('option', 'off') == 'yes'):
            miner = Miner(user=request.user.username)
            mempool = Mempool(user_name=request.user.username)
            miner.save()
            mempool.save()
            return render(request, 'mining.html')
        elif (request.POST.get('option', 'off') == 'no'):
            return render(request, 'mine.html')
    else:
        transactions = get_mempool_transactions(request.user)
        my_dict = {'transactions': transactions}
        return render(request, 'mining.html', context=my_dict)


@login_required
def mined(request):
    my_dict = {'chain': chain_list}
    return render(request, 'mined.html', context=my_dict)


@login_required
def deleteTransaction(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    transaction.delete()
    return redirect('mining')
