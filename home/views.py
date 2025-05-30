"""
Blockchain ledger views.

This module contains view functions for the blockchain simulation:
- Home dashboard
- Wallet management and transactions
- Mining operations
- Blockchain visualization
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import ValidationError
from home.models import Block, Transaction, Mempool, Blockchain, Miner, Wallet
import logging

logger = logging.getLogger(__name__)

# Global variable to store blockchain data for display
# In a production app, this would be stored in cache or database
chain_list = {}


@login_required
def home(request):
    """
    Home dashboard showing user's blockchain status and quick stats.
    """
    context = {
        'user': request.user,
        'title': 'Blockchain Dashboard'
    }
    return render(request, 'home.html', context)


@login_required
def wallet(request):
    """
    Wallet view for creating and managing transactions.
    Handles both GET (display form) and POST (create transaction).
    """
    if request.method == 'POST':
        try:
            # Validate form data
            miner_name = request.POST.get('miner', '').strip()
            receiver = request.POST.get('recieve', '').strip()  # Note: keeping original typo for compatibility
            amount = request.POST.get('amount', '0')
            
            if not miner_name or not receiver or not amount:
                messages.error(request, 'All fields are required.')
                return redirect('wallet')
            
            try:
                amount = int(amount)
                if amount <= 0:
                    messages.error(request, 'Amount must be a positive integer.')
                    return redirect('wallet')
            except ValueError:
                messages.error(request, 'Amount must be a valid number.')
                return redirect('wallet')
            
            # Get or create mempool for the selected miner
            try:
                mempool = Mempool.objects.get(user_name=miner_name)
            except Mempool.DoesNotExist:
                messages.error(request, f'Mempool not found for miner: {miner_name}')
                return redirect('wallet')
            
            # Create new transaction
            transaction = Transaction(
                sender_address=str(request.user),
                receiver_address=receiver,
                amount=amount,
                mempool=mempool
            )
            transaction.save()
            
            # Update mempool transaction count
            mempool.tx_count = Transaction.objects.filter(mempool=mempool).count()
            mempool.save()
            
            messages.success(request, f'Transaction of {amount} sent to {receiver} via {miner_name}!')
            logger.info(f'Transaction created: {request.user} -> {receiver}, amount: {amount}')
            
        except Exception as e:
            logger.error(f'Error creating transaction: {str(e)}')
            messages.error(request, 'An error occurred while creating the transaction.')
            return redirect('wallet')
    
    # Get available miners (limit to 5 for display)
    miners = Miner.objects.filter(is_active=True)[:5]
    if not miners:
        miners = Miner.objects.all()[:5]
    
    context = {
        'miners': miners,
        'title': 'Digital Wallet'
    }
    return render(request, 'wallet.html', context)


@login_required
def mining_block(request):
    """
    Process selected transactions and mine them into a new block.
    """
    if request.method != 'POST':
        return redirect('mining')
    
    try:
        # Check if any transactions were selected for mining
        selected_transactions = []
        for key in request.POST.keys():
            if key.endswith('box'):  # Transaction selection checkboxes end with 'box'
                selected_transactions.append(key[:-3])  # Remove 'box' suffix to get tx_id
        
        if not selected_transactions:
            messages.warning(request, 'Please select at least one transaction to mine.')
            return redirect('mining')
        
        # Get or create blockchain for current user
        blockchain, created = Blockchain.objects.get_or_create(
            user=str(request.user),
            defaults={'genesis': None, 'latest': None}
        )
        
        # Create new block
        new_block = Block(
            miner=request.user.username,
            tx_count=len(selected_transactions)
        )
        
        # Link to previous block if blockchain exists
        if blockchain.latest:
            new_block.previous = blockchain.latest
        
        new_block.save()
        
        # Update blockchain pointers
        if created or not blockchain.genesis:
            blockchain.genesis = new_block
        blockchain.latest = new_block
        blockchain.save()
        
        # Move selected transactions from mempool to block
        transactions_moved = 0
        for tx_id in selected_transactions:
            try:
                transaction = Transaction.objects.get(tx_id=tx_id, mempool__isnull=False)
                old_mempool = transaction.mempool
                
                # Move transaction to block
                transaction.mempool = None
                transaction.block = new_block
                transaction.save()
                
                # Update mempool count
                if old_mempool:
                    old_mempool.tx_count = Transaction.objects.filter(mempool=old_mempool).count()
                    old_mempool.save()
                
                transactions_moved += 1
                
            except Transaction.DoesNotExist:
                logger.warning(f'Transaction {tx_id} not found or already processed')
                continue
        
        # Update miner's stats
        try:
            miner = Miner.objects.get(user=request.user)
            miner.mine_block()
        except Miner.DoesNotExist:
            pass
        
        # Update global chain list for display
        _update_chain_display(blockchain)
        
        messages.success(request, f'Successfully mined block #{new_block.block_id} with {transactions_moved} transactions!')
        logger.info(f'Block mined by {request.user}: Block #{new_block.block_id}, TX count: {transactions_moved}')
        
        return redirect('mined')
        
    except Exception as e:
        logger.error(f'Error mining block: {str(e)}')
        messages.error(request, 'An error occurred while mining the block.')
        return redirect('mining')


@login_required
def mine(request):
    """
    Check if user is a miner and redirect accordingly.
    """
    try:
        miner = Miner.objects.get(user=request.user)
        return redirect('mining')
    except Miner.DoesNotExist:
        context = {'title': 'Become a Miner'}
        return render(request, 'mine.html', context)


@login_required
def mining(request):
    """
    Mining interface for registered miners.
    Handles miner registration and displays pending transactions.
    """
    if request.method == 'POST':
        option = request.POST.get('option', 'off')
        
        if option == 'yes':
            # Register user as a miner
            try:
                miner, created = Miner.objects.get_or_create(
                    user=request.user,
                    defaults={'is_active': True}
                )
                mempool, created = Mempool.objects.get_or_create(
                    user_name=request.user.username,
                    defaults={'tx_count': 0}
                )
                
                if created:
                    messages.success(request, 'You are now registered as a miner!')
                else:
                    messages.info(request, 'You are already a registered miner.')
                
                logger.info(f'User {request.user.username} registered as miner')
                
            except Exception as e:
                logger.error(f'Error registering miner: {str(e)}')
                messages.error(request, 'An error occurred while registering as a miner.')
        
        elif option == 'no':
            context = {'title': 'Mining Setup'}
            return render(request, 'mine.html', context)
    
    # Display mining interface with pending transactions
    try:
        mempool = Mempool.objects.get(user_name=request.user.username)
        pending_transactions = Transaction.objects.filter(mempool=mempool, block__isnull=True)
    except Mempool.DoesNotExist:
        pending_transactions = []
        messages.info(request, 'No mempool found. Please register as a miner first.')
    
    context = {
        'transactions': pending_transactions,
        'title': 'Mining Operations'
    }
    return render(request, 'mining.html', context)


@login_required
def mined(request):
    """
    Display the complete blockchain with all mined blocks.
    """
    context = {
        'chain': chain_list,
        'title': 'Blockchain Explorer'
    }
    return render(request, 'mined.html', context)


@login_required
def delete_transaction(request, pk):
    """
    Delete a specific transaction (only if it's still in mempool).
    """
    try:
        transaction = get_object_or_404(Transaction, pk=pk)
        
        # Only allow deletion of pending transactions
        if transaction.block:
            messages.error(request, 'Cannot delete confirmed transactions.')
            return redirect('mining')
        
        # Update mempool count before deletion
        if transaction.mempool:
            mempool = transaction.mempool
            transaction.delete()
            mempool.tx_count = Transaction.objects.filter(mempool=mempool).count()
            mempool.save()
        else:
            transaction.delete()
        
        messages.success(request, 'Transaction deleted successfully.')
        logger.info(f'Transaction {pk} deleted by {request.user}')
        
    except Exception as e:
        logger.error(f'Error deleting transaction {pk}: {str(e)}')
        messages.error(request, 'An error occurred while deleting the transaction.')
    
    return redirect('mining')


def _update_chain_display(blockchain):
    """
    Helper function to update the global chain display data.
    In a production app, this would use a proper caching mechanism.
    """
    try:
        global chain_list
        chain_list.clear()
        
        all_blocks = blockchain.get_all_blocks()
        for block in all_blocks:
            transactions = Transaction.objects.filter(block=block)
            chain_list[block] = transactions
            
    except Exception as e:
        logger.error(f'Error updating chain display: {str(e)}')
