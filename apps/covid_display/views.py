# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def covid_display(request):
    return render(request, 'home/covid_display.html')
