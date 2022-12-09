# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.wendler import views

urlpatterns = [

    # The home page
    path('wendler.html', views.wendler_view, name='wendler'),

    path('export/', views.some_view, name='exporty'),
    # Matches any html file

]
