from django.test import TestCase
from django.contrib.auth.models import User
from home.models import Block, Transaction, Mempool, Blockchain, Miner, Wallet
from core.utils import create_pending_transaction, validate_mining_request, create_or_get_blockchain


class TransactionTimestampTestCase(TestCase):
    """Test cases for transaction_timestamp functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.mempool = Mempool.objects.create(user_name='testuser')
    
    def test_transaction_timestamp_creation(self):
        """Test that pending transactions get proper transaction_timestamp."""
        transaction = create_pending_transaction(
            sender=self.user,
            receiver='recipient',
            amount=100,
            mempool=self.mempool
        )
        self.assertIsNotNone(transaction.transaction_timestamp)
        self.assertEqual(transaction.mempool, self.mempool)


class MempoolProcessingTestCase(TestCase):
    """Test cases for mempool/pending queue functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='miner', password='testpass')
    
    def test_mempool_validation(self):
        """Test validation of mining requests with transaction boxes."""
        # Valid request with transaction box
        valid_post_data = {'123box': 'selected', 'other_field': 'value'}
        self.assertTrue(validate_mining_request(valid_post_data))
        
        # Invalid request without transaction box
        invalid_post_data = {'field1': 'value', 'field2': 'value'}
        self.assertFalse(validate_mining_request(invalid_post_data))


class BlockchainTestCase(TestCase):
    """Test cases for blockchain and transaction_count functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='blockuser', password='testpass')
    
    def test_blockchain_creation_with_transaction_timestamp(self):
        """Test blockchain creation includes proper transaction_timestamp on genesis block."""
        blockchain, is_new = create_or_get_blockchain(self.user)
        self.assertTrue(is_new)
        self.assertIsNotNone(blockchain.genesis)
        self.assertIsNotNone(blockchain.genesis.transaction_timestamp)
        self.assertEqual(blockchain.genesis.transaction_count, 0)
