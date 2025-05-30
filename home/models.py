"""
Blockchain ledger models.

This module contains the core models for the blockchain simulation:
- Mempool: Manages pending transactions
- Block: Represents individual blocks in the blockchain
- Transaction: Represents transactions between users
- Blockchain: Links blocks together in a chain
- Wallet: User wallet information
- Miner: Users who can mine blocks
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Mempool(models.Model):
    """
    Mempool stores pending transactions before they are added to a block.
    Each user (miner) has their own mempool.
    """
    user_name = models.CharField(max_length=200, help_text="Username of the miner")
    tx_count = models.PositiveIntegerField(default=0, help_text="Number of transactions in mempool")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mempool"
        verbose_name_plural = "Mempools"
        ordering = ['-updated_at']

    def __str__(self):
        return f"Mempool for {self.user_name} ({self.tx_count} transactions)"


class Block(models.Model):
    """
    Block represents a single block in the blockchain.
    Contains transactions and links to previous block.
    """
    block_id = models.AutoField(primary_key=True)
    tx_count = models.PositiveIntegerField(default=0, help_text="Number of transactions in this block")
    timestamp = models.DateTimeField(help_text="When the block was created")
    previous = models.OneToOneField(
        'self', 
        null=True, 
        blank=True, 
        related_name="next", 
        on_delete=models.CASCADE,
        help_text="Reference to the previous block in the chain"
    )
    miner = models.CharField(max_length=200, blank=True, help_text="Username of the miner who created this block")

    class Meta:
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        """Automatically set timestamp when saving a new block."""
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Block #{self.block_id} (TX: {self.tx_count})"

    def get_transactions(self):
        """Get all transactions in this block."""
        return self.transaction_set.all()


class Transaction(models.Model):
    """
    Transaction represents a transfer of value between two addresses.
    Can be in mempool (pending) or in a block (confirmed).
    """
    tx_id = models.AutoField(primary_key=True)
    sender_address = models.CharField(max_length=200, help_text="Address sending the transaction")
    receiver_address = models.CharField(max_length=200, help_text="Address receiving the transaction")
    amount = models.PositiveIntegerField(default=0, help_text="Amount being transferred")
    timestamp = models.DateTimeField(help_text="When the transaction was created")
    
    # Transaction can be either in mempool or in a block, but not both
    block = models.ForeignKey(
        Block, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        help_text="Block containing this transaction (null if in mempool)"
    )
    mempool = models.ForeignKey(
        Mempool, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        help_text="Mempool containing this transaction (null if confirmed)"
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        """Automatically set timestamp when creating a new transaction."""
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        status = "Confirmed" if self.block else "Pending"
        return f"TX #{self.tx_id}: {self.sender_address} → {self.receiver_address} ({self.amount}) [{status}]"

    @property
    def is_confirmed(self):
        """Check if transaction is confirmed (in a block)."""
        return self.block is not None

    @property
    def is_pending(self):
        """Check if transaction is pending (in mempool)."""
        return self.mempool is not None


class Blockchain(models.Model):
    """
    Blockchain represents the entire chain of blocks for a user.
    Links the genesis block to the latest block.
    """
    user = models.CharField(max_length=200, help_text="Owner of this blockchain")
    genesis = models.OneToOneField(
        Block, 
        null=True, 
        blank=True, 
        related_name="init_chain", 
        on_delete=models.CASCADE,
        help_text="First block in the chain"
    )
    latest = models.OneToOneField(
        Block, 
        null=True, 
        blank=True, 
        related_name="end_chain", 
        on_delete=models.CASCADE,
        help_text="Most recent block in the chain"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Blockchain"
        verbose_name_plural = "Blockchains"
        ordering = ['-created_at']

    def __str__(self):
        return f"Blockchain for {self.user}"

    def get_chain_length(self):
        """Calculate the length of the blockchain."""
        if not self.genesis:
            return 0
        
        count = 1
        current = self.genesis
        try:
            while hasattr(current, 'next') and current.next:
                current = current.next
                count += 1
        except AttributeError:
            pass
        return count

    def get_all_blocks(self):
        """Get all blocks in the chain as a list."""
        if not self.genesis:
            return []
        
        blocks = [self.genesis]
        current = self.genesis
        try:
            while hasattr(current, 'next') and current.next:
                current = current.next
                blocks.append(current)
        except AttributeError:
            pass
        return blocks


class Wallet(models.Model):
    """
    Wallet represents a user's digital wallet.
    Stores user information and balance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="User who owns this wallet")
    balance = models.PositiveIntegerField(default=1000, help_text="Current wallet balance")
    address = models.CharField(max_length=200, unique=True, help_text="Unique wallet address")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ['-created_at']

    def __str__(self):
        return f"Wallet for {self.user.username} (Balance: {self.balance})"

    def can_send(self, amount):
        """Check if wallet has sufficient balance for a transaction."""
        return self.balance >= amount

    def send_transaction(self, amount):
        """Deduct amount from wallet balance."""
        if self.can_send(amount):
            self.balance -= amount
            self.save()
            return True
        return False

    def receive_transaction(self, amount):
        """Add amount to wallet balance."""
        self.balance += amount
        self.save()


class Miner(models.Model):
    """
    Miner represents a user who can mine blocks.
    Links to Django's User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="User who is a miner")
    is_active = models.BooleanField(default=True, help_text="Whether the miner is currently active")
    blocks_mined = models.PositiveIntegerField(default=0, help_text="Total number of blocks mined")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Miner"
        verbose_name_plural = "Miners"
        ordering = ['-blocks_mined']

    def __str__(self):
        return f"Miner: {self.user.username} ({self.blocks_mined} blocks)"

    def mine_block(self):
        """Increment the blocks mined counter."""
        self.blocks_mined += 1
        self.save()
