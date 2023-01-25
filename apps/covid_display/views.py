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

import pandas as pd


@login_required(login_url="/login/")
def covid_display(request):
    '''
    url = "https://covid-193.p.rapidapi.com/history"

    headers = {
        "X-RapidAPI-Key": "21c4febd1cmsh939ae64962c6da3p1994cajsn4ac28b07c9c7",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com",
    }

    querystring = {"country": "S-Korea", "day": "2020-06-02"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    '''
    df = pd.read_csv('owid-covid-data.csv')
    df = df[df.location == 'South Korea']

    print(df)

    # convert reponse data into json
    users = {"sd":"sdsd"}

    fig = go.Figure()
    scatter = go.Scatter(x=df.date, y=df.new_cases,
                         mode='lines', name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)
    plt_div = plot(fig, output_type='div')

    context = {'plt_div': plt_div, 'users': users}

    return render(request, 'home/covid_display.html', context)
