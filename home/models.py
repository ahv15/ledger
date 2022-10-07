from django.db import models
from django.utils import timezone


class Memepool(models.Model):
    user_name = models.CharField(max_length=200)
    txcount = models.IntegerField(default=0)

    def __str__(self):
        return str('Memepool')


class Block(models.Model):
    blockid = models.AutoField(primary_key=True)
    txcount = models.IntegerField(default=0)
    time_stamp = models.DateTimeField()
    previous = models.OneToOneField(
        'self', null=True, blank=True, related_name="next", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.time_stamp = timezone.now()
        return super(Block, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.blockid)


class Transaction(models.Model):
    txid = models.AutoField(primary_key=True)
    sendAddr = models.CharField(max_length=200)
    receiveAddr = models.CharField(max_length=200)
    amount = models.IntegerField(default=0)
    time_stamp = models.DateTimeField()
    block = models.ForeignKey(
        Block, on_delete=models.CASCADE, blank=True, null=True)
    memepool = models.ForeignKey(
        Memepool, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.time_stamp = timezone.now()
        return super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.txid)


class Blockchain(models.Model):
    user = models.CharField(max_length=200)
    genesis = models.OneToOneField(
        Block, null=True, blank=True, related_name="init_chain", on_delete=models.CASCADE)
    latest = models.OneToOneField(
        Block, null=True, blank=True, related_name="end_chain", on_delete=models.CASCADE)

    def __str__(self):
        return 'Main Chain'


class Wallet(models.Model):
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.user


class Miner(models.Model):
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.user
