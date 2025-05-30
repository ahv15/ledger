"""
Django admin configuration for blockchain models.

This module registers the blockchain models with the Django admin interface
for easy management and debugging.
"""

from django.contrib import admin
from .models import Block, Transaction, Mempool, Blockchain, Miner, Wallet


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    """
    Admin interface for Block model.
    """
    list_display = ('block_id', 'miner', 'tx_count', 'timestamp', 'previous')
    list_filter = ('timestamp', 'miner')
    search_fields = ('block_id', 'miner')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Block Information', {
            'fields': ('block_id', 'miner', 'tx_count', 'timestamp')
        }),
        ('Chain Links', {
            'fields': ('previous',),
            'description': 'Links to other blocks in the chain'
        })
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for Transaction model.
    """
    list_display = ('tx_id', 'sender_address', 'receiver_address', 'amount', 'timestamp', 'is_confirmed')
    list_filter = ('timestamp', 'block', 'mempool')
    search_fields = ('tx_id', 'sender_address', 'receiver_address')
    readonly_fields = ('timestamp', 'is_confirmed', 'is_pending')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('tx_id', 'sender_address', 'receiver_address', 'amount', 'timestamp')
        }),
        ('Status', {
            'fields': ('block', 'mempool', 'is_confirmed', 'is_pending'),
            'description': 'Transaction can be either in a block (confirmed) or mempool (pending)'
        })
    )


@admin.register(Mempool)
class MempoolAdmin(admin.ModelAdmin):
    """
    Admin interface for Mempool model.
    """
    list_display = ('user_name', 'tx_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user_name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)


@admin.register(Blockchain)
class BlockchainAdmin(admin.ModelAdmin):
    """
    Admin interface for Blockchain model.
    """
    list_display = ('user', 'genesis', 'latest', 'get_chain_length', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user',)
    readonly_fields = ('created_at', 'get_chain_length')
    ordering = ('-created_at',)
    
    def get_chain_length(self, obj):
        """Display chain length in admin list."""
        return obj.get_chain_length()
    get_chain_length.short_description = 'Chain Length'


@admin.register(Miner)
class MinerAdmin(admin.ModelAdmin):
    """
    Admin interface for Miner model.
    """
    list_display = ('user', 'is_active', 'blocks_mined', 'joined_at')
    list_filter = ('is_active', 'joined_at')
    search_fields = ('user__username',)
    readonly_fields = ('joined_at',)
    ordering = ('-blocks_mined',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Admin interface for Wallet model.
    """
    list_display = ('user', 'address', 'balance', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'address')
    readonly_fields = ('created_at',)
    ordering = ('-balance',)
    
    fieldsets = (
        ('Wallet Owner', {
            'fields': ('user', 'address', 'created_at')
        }),
        ('Balance', {
            'fields': ('balance',),
            'description': 'Current wallet balance'
        })
    )
