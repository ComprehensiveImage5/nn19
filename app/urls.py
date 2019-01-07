"""nn19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from .views import home_view, profile_view, user_view, status_view, logout_view, fallen_view, fighting_view

urlpatterns = [
    path('', home_view),
    path('profile', profile_view),
    path('soldier', user_view),
    path('status', status_view),
    path('logout', logout_view),
    path('fallen', fallen_view),
    path('fighting', fighting_view)
]
