# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .forms import WendlerForm

'''@login_required(login_url="/login/")
def wendler_view(request):
    context = {'segment': 'wendler',
               'number':3}
    html_template = loader.get_template('home/wendler.html')
    return HttpResponse(html_template.render(context, request))'''


@login_required(login_url="/login/")
def wendler_view(request):
    if request.method == 'POST':

        form = WendlerForm(request.POST)

        if form.is_valid():
            # Takes the input of one Rep Max and assigns it to the number variable
            number = int(request.POST['oneRepMax'])

            # Initializes a dictionary for containing calculated exercises
            calculated_dict = {
                'week1': {'set1': str((number * 0.40 - 20) / 2) + 'kgx5',
                          'set2': str((number * 0.65 - 20) / 2) + 'kgx5',
                          'set3': str((number * 0.75 - 20) / 2) + 'kgx5',
                          'set4': str((number * 0.85 - 20) / 2) + 'kgx5'},

                'week2': {'set1': str((number * 0.40 - 20) / 2) + 'kgx3',
                          'set2': str((number * 0.70 - 20) / 2) + 'kgx3',
                          'set3': str((number * 0.80 - 20) / 2) + 'kgx3',
                          'set4': str((number * 0.90 - 20) / 2) + 'kgx3'},

                'week3': {'set1': str((number * 0.40 - 20) / 2) + 'kgx5',
                          'set2': str((number * 0.75 - 20) / 2) + 'kgx5',
                          'set3': str((number * 0.85 - 20) / 2) + 'kgx3',
                          'set4': str((number * 0.95 - 20) / 2) + 'kgx1'},

                'week4': {'set1': str((number * 0.40 - 20) / 2) + 'kgx5',
                          'set2': str((number * 0.40 - 20) / 2) + 'kgx5',
                          'set3': str((number * 0.50 - 20) / 2) + 'kgx5',
                          'set4': str((number * 0.60 - 20) / 2) + 'kgx5'},
            }

            return render(request, 'home/wendler.html',
                          {'form': form, 'number': number, 'calculated_dict': calculated_dict})

    else:
        form = WendlerForm()

    return render(request, 'home/wendler.html', {'form': form})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:wendler'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
