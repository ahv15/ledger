"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views
from home import views as home_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path('admin/', admin.site.urls),
    path('home/', home_views.home, name='home'),
    path('mining_block', home_views.mining_block, name='mining_block'),
    path('wallet', home_views.wallet, name='wallet'),
    path('mine', home_views.mine, name='mine'),
    path('mining', home_views.mining, name='mining'),
    path('mined', home_views.mined, name='mined'),
    path('delete/<pk>', home_views.deleteTransaction, name='deletetransaction')
]
