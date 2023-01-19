# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.covid_display import views

urlpatterns = [

    # The home page
    path('covid_display.html', views.covid_display, name='covid_display'),
]
