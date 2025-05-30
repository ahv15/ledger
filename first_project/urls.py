"""
Blockchain Ledger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from users import views as user_views
from home import views as home_views


urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', user_views.login, name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout, name='logout'),
    
    # Main application URLs
    path('', RedirectView.as_view(url='/home/', permanent=True)),  # Redirect root to home
    path('home/', home_views.home, name='home'),
    
    # Wallet and transaction URLs
    path('wallet/', home_views.wallet, name='wallet'),
    
    # Mining URLs
    path('mine/', home_views.mine, name='mine'),
    path('mining/', home_views.mining, name='mining'),
    path('mining/block/', home_views.mining_block, name='mining_block'),
    path('mined/', home_views.mined, name='mined'),
    
    # Transaction management
    path('transaction/delete/<int:pk>/', home_views.delete_transaction, name='delete_transaction'),
]

# Custom error handlers (optional - for production)
# handler404 = 'home.views.handler404'
# handler500 = 'home.views.handler500'
