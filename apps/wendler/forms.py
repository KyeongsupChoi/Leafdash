# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms



class WendlerForm(forms.Form):
    oneRepMax = forms.IntegerField()