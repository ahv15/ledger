from django.db import models
from django.utils import timezone


class Mempool(models.Model):
    """Represents a mempool for pending transactions."""
    user_name = models.CharField(max_length=200)
    transaction_count = models.IntegerField(default=0)

    def __str__(self):
        return str('Mempool')


class Block(models.Model):
    """Represents a block in the blockchain."""
    blockid = models.AutoField(primary_key=True)
    transaction_count = models.IntegerField(default=0)
    transaction_timestamp = models.DateTimeField()
    previous = models.OneToOneField(
        'self', null=True, blank=True, related_name="next", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.transaction_timestamp = timezone.now()
        return super(Block, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.blockid)


class Transaction(models.Model):
    """Represents a transaction in the ledger."""
    txid = models.AutoField(primary_key=True)
    sendAddr = models.CharField(max_length=200)
    receiveAddr = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    transaction_timestamp = models.DateTimeField()
    block = models.ForeignKey(
        Block, on_delete=models.CASCADE, blank=True, null=True)
    mempool = models.ForeignKey(
        Mempool, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.transaction_timestamp = timezone.now()
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.txid)


class Blockchain(models.Model):
    """Represents the main blockchain structure."""
    user = models.CharField(max_length=200)
    genesis = models.OneToOneField(
        Block, null=True, blank=True, related_name="init_chain", on_delete=models.CASCADE)
    latest = models.OneToOneField(
        Block, null=True, blank=True, related_name="end_chain", on_delete=models.CASCADE)

    def __str__(self):
        return 'Main Chain'


class Wallet(models.Model):
    """Represents a user's wallet."""
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.user


class Miner(models.Model):
    """Represents a miner in the network."""
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.user
