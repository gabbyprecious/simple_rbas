"""simple_rbas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('user-auth/', LoginView.as_view({"post": "login"}), name = "user-login"),
    path('user-signup/', SignUpView.as_view({"post": "create"}), name = "user-signup"),
    path('all-user/', AllUser.as_view({"post": "get"}), name = "all-users"),
    path('authenticated-user/', OnlyAuthenticatedUser.as_view({"post": "get"}), name = "authenticated-user"),
    path('only-staff/', OnlyStaffOwnerUser.as_view({"post": "get"}), name = "only-staff"),
    path('only-admin/', OnlyAdminStaffOwnerUser.as_view({"post": "get"}), name = "only-admin"),
    path('only-investor-owner/', OnlyInvestorAndOwnerUser.as_view({"post": "get"}), name = "only-investor-owner"),
    path('only-owner/', OnlyOwnerUser.as_view({"post": "get"}), name = "only-owner"),
]
