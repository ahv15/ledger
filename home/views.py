from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from home.models import Block, Transaction, Memepool, Blockchain, Miner, Wallet


import sys
# Create your views here.
chain_list = {}


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def wallet(request):
    if request.method == 'POST':
        print(request.POST)
        memepool = Memepool.objects.filter(user_name=request.POST['miner'])[0]
        tx = Transaction(sendAddr=request.user,
                         receiveAddr=request.POST['reciever'],  amount=request.POST['amount'], memepool=memepool)
        tx.save()
    if (len(Miner.objects.filter()) > 5):
        miners = Miner.objects.filter()[0:4]
    else:
        miners = Miner.objects.filter()[0:]
    my_dict = {'miners': miners}
    return render(request, 'wallet.html', context=my_dict)


@login_required
def mining_block(request):
    if request.method == 'POST':
        if (len(request.POST.keys()) > 0):
            check = False
            for key in request.POST.keys():
                if (key[-3:] == 'box'):
                    check = True
            if (not check):
                return redirect('mining')
            chain = Blockchain.objects.filter(user=request.user)
            block = Block(previous=None)
            if (len(chain) == 0):
                chain = Blockchain(user=request.user,
                                   genesis=block, latest=block)
            else:
                chain = chain[0]
                latest = chain.latest
                block.previous = latest
                chain.latest = block

            block.save()
            chain.save()

            for key in request.POST.keys():
                if (key[-3:] == 'box'):
                    tx = Transaction.objects.filter(txid=key[0:-3])[0]
                    tx.memepool = None
                    tx.block = block
                    tx.save()
        first = chain.genesis
        list_ = [first]
        try:
            while (first.next != []):
                print(first)
                list_.append(first.next)
                first = first.next
        except:
            print(list_)
        for block in list_:
            tx = Transaction.objects.filter(block=block)[:]
            chain_list[block] = tx
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
            memepool = Memepool(user_name=request.user.username)
            miner.save()
            memepool.save()
            return render(request, 'mining.html')
        elif (request.POST.get('option', 'off') == 'no'):
            return render(request, 'mine.html')
    else:
        memepool = Memepool.objects.filter(user_name=request.user)[0]
        transactions = Transaction.objects.filter(memepool=memepool)
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
