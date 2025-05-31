# Django Blockchain Ledger

Simple blockchain-style ledger with mempool and transaction tracking

## Overview

This Django application mimics the basic functionality of a blockchain ledger system. It includes a mempool for managing pending transactions, balance tracking across wallets, and block record storage for confirmed transactions. Users can submit transactions to the mempool, mine blocks to confirm pending transactions, and view the complete ledger state through a web interface.

## Installation

### Requirements
- Python 3.8+
- Django 3.2+

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahv15/ledger.git
   cd ledger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Navigate to `http://localhost:8000` in your web browser
   - Register a new user account or login with existing credentials

## Usage

The application provides a complete workflow for blockchain-style ledger operations:

1. **User Registration & Authentication**: Create user accounts and login to access the ledger
2. **Wallet Management**: View available miners and submit transactions to the mempool
3. **Mining Operations**: Become a miner to process pending transactions and create new blocks
4. **Block Confirmation**: Select pending transactions from mempool and mine them into blocks
5. **Ledger Visualization**: View the complete blockchain with all confirmed transactions

### Basic Workflow

1. Register and login to create a user account
2. Navigate to the wallet page to submit new transactions
3. Choose a miner and specify recipient address and amount
4. Access mining interface to become a miner and view pending transactions
5. Select transactions from mempool and mine them into a new block
6. View the complete blockchain with all confirmed transactions

## Structure

The project is organized into the following key modules:

- **`core/`**: Core blockchain utilities and helper functions
  - `utils.py`: Consolidated functions for mempool processing, block creation, transaction validation, and blockchain traversal
  
- **`home/`**: Main application logic
  - `models.py`: Defines core models including `Transaction`, `Block`, `Mempool`, `Blockchain`, `Miner`, and `Wallet`
  - `views.py`: Provides endpoints for wallet operations, mining interface, block creation, and ledger visualization
  - `admin.py`: Django admin interface configuration
  
- **`users/`**: User authentication and management
  - `views.py`: User registration, login, and logout functionality
  - `forms.py`: Django forms for user signup and login
  - `models.py`: User-related model extensions (currently empty)

- **`first_project/`**: Django project configuration
  - `settings.py`: Project settings and installed apps configuration
  - `urls.py`: URL routing for the entire application
  
- **`templates/`**: HTML templates for the web interface
- **`static/`**: CSS, JavaScript, and image assets

## Tests

Run the existing test suite to verify ledger functionality:

```bash
# Using Django's built-in test runner
python manage.py test

# Alternative: Using pytest (if installed)
pytest
```

The tests cover mempool handling, transaction validation, block creation, and blockchain consistency checks.

## Author

**Harshit**  
Email: 52852877+ahv15@users.noreply.github.com  
GitHub: [https://github.com/ahv15/ledger](https://github.com/ahv15/ledger)

## Scope & Exclusions

This project implements a simplified blockchain-style ledger for educational and demonstration purposes. The following blockchain features are **excluded** from this implementation:

- **No Proof-of-Work or Proof-of-Stake consensus mechanisms** - Mining is simplified without computational puzzles or stake validation
- **No peer-to-peer networking or distributed node synchronization** - Operates as a single-node system without network protocols
- **No cryptographic hashing of blocks or transactions** - Uses simple database IDs instead of cryptographic hashes
- **No smart contract execution or scripting languages** - Limited to basic transaction processing
- **No digital signatures or transaction verification** - Transactions are processed without cryptographic validation
- **No merkle trees or block header structures** - Simplified block storage without advanced data structures
- **No difficulty adjustment or mining rewards** - Mining operations are instantaneous without economic incentives

The focus is on demonstrating the core concepts of transaction mempool management, block creation, and ledger state tracking in a web application format.
