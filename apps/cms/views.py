from django.shortcuts import render
from apps.cms.models import BlogPage

# Create your views here.


def blog_list(request):
    context = {
        'blogs': BlogPage.objects.all(),
        'segment': 'cms',
        'parent': 'apps'
    }
    return render(request, 'apps/cms/blog_list.html', context)