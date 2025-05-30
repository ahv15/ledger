# Blockchain Ledger Simulation

A Django-based blockchain simulation application that demonstrates the core concepts of cryptocurrency transactions, mining, and blockchain technology.

## Features

- **User Authentication**: Secure user registration and login system
- **Digital Wallet**: Create and manage cryptocurrency wallets
- **Transaction System**: Send and receive digital currency between users
- **Mining Simulation**: Participate in blockchain mining to validate transactions
- **Blockchain Visualization**: View the complete blockchain with all mined blocks
- **Mempool Management**: Handle pending transactions before they are mined

## Technology Stack

- **Backend**: Django 3.2+
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django's built-in authentication system

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahv15/ledger.git
   cd ledger
   ```

2. Create a virtual environment:
   ```bash
   python -m venv blockchain_env
   source blockchain_env/bin/activate  # On Windows: blockchain_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000` in your browser

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Setup Mining**: Navigate to the mining section and enable mining for your account
3. **Create Transactions**: Use the wallet to send currency to other users
4. **Mine Blocks**: Process pending transactions by mining new blocks
5. **View Blockchain**: Examine the complete blockchain history

## Project Structure

```
ledger/
├── first_project/          # Main Django project settings
├── home/                   # Core blockchain functionality
│   ├── models.py          # Database models (Block, Transaction, etc.)
│   └── views.py           # Business logic and views
├── users/                  # User authentication
├── templates/              # HTML templates
├── static/                 # CSS, JS, and static files
└── manage.py              # Django management script
```

## Models Overview

- **Block**: Represents a block in the blockchain
- **Transaction**: Individual transactions between users
- **Mempool**: Manages pending transactions
- **Blockchain**: Links blocks together in a chain
- **Miner**: Users who can mine blocks
- **Wallet**: User wallet information

## Contributing

This is an educational project demonstrating blockchain concepts. Feel free to fork and experiment with the code.

## License

This project is open source and available under the MIT License.
