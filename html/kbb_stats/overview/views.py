from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Cars
from .plot import plot_data
from .style_table import get_style_table
import os


# Create your views here.
def index(request):
    if request.method == 'GET':
        all_makes = Cars.objects.values_list('make', flat=True).distinct().order_by('make')
        context = {'all_makes': all_makes}
        return render(request, 'overview/index.html', context)
    elif request.method == 'POST':
        make = request.POST['select_make']
        return HttpResponseRedirect("/kbb/{}/".format(make))

def make(request, make):
    if request.method == 'GET':
        all_models = Cars.objects.filter(make__exact=make).values_list('model', flat=True).distinct().order_by('model')
        context = {'make': make, 'all_models': all_models}
        return render(request, 'overview/make.html', context)
    elif request.method == 'POST':
        model = request.POST['select_model']
        return HttpResponseRedirect("/kbb/{}/{}/".format(make, model))

def model(request, make, model):
    query_data = Cars.objects.filter(make__exact=make, model__exact=model)

    img_file = "../../data/model_images/{}/{}".format(make, model)
    if os.path.isfile(img_file + '.jpg'):
        img_file = "overview/model/{}/{}.jpg".format(make, model)
    elif os.path.isfile(img_file + '.png'):
        img_file = "overview/model/{}/{}.png".format(make, model)
    else:
        img_file = ''

    plot_file = plot_data(make, model, query_data)
    style_title, style_table = get_style_table(make, model, query_data)

    context = {'make': make, 'model': model, 'img_file': img_file, 'plot_file': plot_file, 'style_title': style_title, 'style_table': style_table}
    return render(request, 'overview/model.html', context)

