from django.shortcuts import render
from apps.common.models import Sales
from django.core import serializers


# Create your views here.

def index(request):
    sales = serializers.serialize('json', Sales.objects.all())
    context = {
        'segment'  : 'charts',
        'parent'   : 'apps',
        'sales': sales
    }
    return render(request, 'apps/charts.html', context)
