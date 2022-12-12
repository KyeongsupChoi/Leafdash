# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .forms import WendlerForm
from reportlab.pdfgen import canvas
import io


'''@login_required(login_url="/login/")
def wendler_view(request):
    context = {'segment': 'wendler',
               'number':3}
    html_template = loader.get_template('home/wendler.html')
    return HttpResponse(html_template.render(context, request))'''

zoop = 2

@login_required(login_url="/login/")
def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    print(zoop)

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    p.drawString(100, 100, str(zoop))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@login_required(login_url="/login/")
def wendler_view(request):
    if request.method == 'POST':

        form = WendlerForm(request.POST)

        if form.is_valid():

            # Takes the input of one Rep Max and assigns it to the number variable
            number = int(request.POST['oneRepMax'])
            global zoop
            zoop = number

            # The list of percentages from the Wendler 531 regimen
            percentage_list = [0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

            # Initializes a dictionary for containing calculated exercise weights
            calculated_dict = {}

            # Loop for iterating over percentage list and number to propagate calculated_dict
            for num in percentage_list:

                # Multiplies One Rep Max with Percentage then Subtracts empty bar weight and Divides by two for both sides
                calc_num = (number * num - 20) / 2

                # Conditional for rounding down to the nearest 2.5 kg (smallest plate)
                if (calc_num % 2.5) < 1.25:
                    calc_num = calc_num - (calc_num % 2.5)

                # Conditional for rounding up to the nearest 2.5 kg (smallest plate)
                else:
                    calc_num = calc_num + 2.5 - (calc_num % 2.5)

                # Assigning weight value to the percentage key
                calculated_dict[num] = calc_num

            # Initializes a dictionary for containing calculated exercise sets
            exercise_dict = {
                'week1': {'set1': str(calculated_dict[0.4]) + 'kgx5',
                          'set2': str(calculated_dict[0.65]) + 'kgx5',
                          'set3': str(calculated_dict[0.75]) + 'kgx5',
                          'set4': str(calculated_dict[0.85]) + 'kgx5'},

                'week2': {'set1': str(calculated_dict[0.4]) + 'kgx3',
                          'set2': str(calculated_dict[0.7]) + 'kgx3',
                          'set3': str(calculated_dict[0.8]) + 'kgx3',
                          'set4': str(calculated_dict[0.9]) + 'kgx3'},

                'week3': {'set1': str(calculated_dict[0.4]) + 'kgx5',
                          'set2': str(calculated_dict[0.75]) + 'kgx5',
                          'set3': str(calculated_dict[0.85]) + 'kgx3',
                          'set4': str(calculated_dict[0.95]) + 'kgx1'},

                'week4': {'set1': str(calculated_dict[0.4]) + 'kgx5',
                          'set2': str(calculated_dict[0.4]) + 'kgx5',
                          'set3': str(calculated_dict[0.5]) + 'kgx5',
                          'set4': str(calculated_dict[0.6]) + 'kgx5'},
            }

            zoop = exercise_dict

            return render(request, 'home/wendler.html',
                          {'form': form, 'number': number, 'calculated_dict': exercise_dict})

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
