# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import requests
from plotly.offline import plot
import plotly.graph_objs as go


@login_required(login_url="/login/")
def covid_display(request):
    response = requests.get('https://api.covid19api.com/country/south-korea/status/confirmed?from=2020-03-01T00:00:00Z&to=2020-04-01T00:00:00Z')
    # convert reponse data into json
    users = response.json()

    fig = go.Figure()
    scatter = go.Scatter(x=[0, 1, 2, 3], y=[0, 1, 2, 3],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    plt_div = plot(fig, output_type='div')

    context = {'plt_div': plt_div, 'users': users}

    return render(request, 'home/covid_display.html', context)
