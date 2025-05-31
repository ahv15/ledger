"""
Core utilities for blockchain-style ledger operations.

This module contains consolidated helper functions for:
- Pending transaction validation and processing
- Block creation and mining operations
- Transaction serialization and mempool management
- Balance calculations and blockchain traversal
"""

from django.utils import timezone
from home.models import Block, Transaction, Mempool, Blockchain


def create_pending_transaction(sender, receiver, amount, mempool):
    """
    Creates a pending transaction in the mempool/pending queue.
    
    Args:
        sender: User sending the transaction
        receiver: User receiving the transaction  
        amount: Transaction amount
        mempool: Mempool instance to add pending transaction to
        
    Returns:
        Transaction: Created transaction instance with transaction_timestamp
    """
    transaction = Transaction(
        sendAddr=sender,
        receiveAddr=receiver,
        amount=amount,
        mempool=mempool
    )
    transaction.save()
    return transaction


def validate_mining_request(post_data):
    """
    Validates if mining request contains valid transaction selections for mempool processing.
    
    Args:
        post_data: POST data from mining request
        
    Returns:
        bool: True if valid mining request with transaction boxes, False otherwise
    """
    if len(post_data.keys()) <= 0:
        return False
        
    has_transaction_box = False
    for key in post_data.keys():
        if key[-3:] == 'box':
            has_transaction_box = True
            break
            
    return has_transaction_box


def create_or_get_blockchain(user):
    """
    Creates a new blockchain for user or returns existing one with proper transaction_timestamp.
    
    Args:
        user: User to create/get blockchain for
        
    Returns:
        tuple: (blockchain_instance, is_new_blockchain)
    """
    existing_chain = Blockchain.objects.filter(user=user)
    
    if len(existing_chain) == 0:
        # Create genesis block with transaction_timestamp
        genesis_block = Block(previous=None)
        genesis_block.save()
        
        # Create blockchain with genesis
        blockchain = Blockchain(
            user=user,
            genesis=genesis_block,
            latest=genesis_block
        )
        blockchain.save()
        return blockchain, True
    else:
        return existing_chain[0], False


def mine_transactions_to_block(blockchain, selected_transaction_ids):
    """
    Mines selected pending transactions from mempool into a new block.
    
    Args:
        blockchain: Blockchain instance to add block to
        selected_transaction_ids: List of transaction IDs to mine from mempool
        
    Returns:
        Block: Newly created block containing transactions with transaction_timestamp
    """
    # Create new block with transaction_timestamp
    latest_block = blockchain.latest
    new_block = Block(previous=latest_block)
    new_block.save()
    
    # Update blockchain latest pointer
    blockchain.latest = new_block
    blockchain.save()
    
    # Move pending transactions from mempool to block
    for tx_id in selected_transaction_ids:
        try:
            transaction = Transaction.objects.filter(txid=tx_id)[0]
            transaction.mempool = None
            transaction.block = new_block
            transaction.save()
        except (IndexError, Transaction.DoesNotExist):
            continue
            
    return new_block


def build_blockchain_list(blockchain):
    """
    Builds ordered list of blocks in blockchain with their transactions and transaction_count.
    
    Args:
        blockchain: Blockchain instance to traverse
        
    Returns:
        dict: Dictionary mapping blocks to their transactions
    """
    chain_list = {}
    current_block = blockchain.genesis
    block_list = [current_block]
    
    try:
        while hasattr(current_block, 'next') and current_block.next:
            current_block = current_block.next
            block_list.append(current_block)
    except Exception:
        # Handle any traversal issues gracefully
        pass
    
    # Build transactions for each block
    for block in block_list:
        transactions = Transaction.objects.filter(block=block)[:]
        chain_list[block] = transactions
        
    return chain_list


def get_mempool_transactions(user):
    """
    Retrieves all pending transactions for a user's mempool/pending queue.
    
    Args:
        user: User to get mempool pending transactions for
        
    Returns:
        QuerySet: Pending transactions in mempool
    """
    try:
        mempool = Mempool.objects.filter(user_name=user)[0]
        return Transaction.objects.filter(mempool=mempool)
    except (IndexError, Mempool.DoesNotExist):
        return Transaction.objects.none()


def calculate_transaction_timestamp():
    """
    Calculates current transaction_timestamp for transactions.
    
    Returns:
        datetime: Current timezone-aware transaction_timestamp
    """
    return timezone.now()
