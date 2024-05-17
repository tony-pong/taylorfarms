from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def dashboard_view(request):
    context = {
        'segment': 'dashboard',
    }
    return render(request, "dashboard/index.html", context)

@login_required
def failures_view(request):
    context = {
        'segment': 'failures',  # This should uniquely identify the failures page
    }
#    return render(request, 'failures/main_page.html', context)
    return render(request, 'failures/snapshots.html', context)


@login_required
def starter(request):
    context = {}
    return render(request, "pages/starter.html", context)

# Layout
@login_required
def stacked(request):
    context = {
        'segment': 'stacked',
        'parent': 'layouts'
    }
    return render(request, 'pages/layouts/stacked.html', context)

@login_required
def sidebar(request):
    context = {
        'segment': 'sidebar',
        'parent': 'layouts'
    }
    return render(request, 'pages/layouts/sidebar.html', context)

# CRUD
@login_required
def products(request):
    context = {
        'segment': 'products',
        'parent': 'crud'
    }
    return render(request, 'pages/CRUD/products.html', context)

@login_required
def users(request):
    context = {
        'segment': 'users',
        'parent': 'crud'
    }
    return render(request, 'pages/CRUD/users.html', context)

# Pages
@login_required
def pricing(request):
    return render(request, 'pages/pricing.html')

@login_required
def maintenance(request):
    return render(request, 'pages/maintenance.html')

@login_required
def error_404(request):
    return render(request, 'pages/404.html')

@login_required
def error_500(request):
    return render(request, 'pages/500.html')

@login_required
def settings_view(request):
    context = {
        'segment': 'settings',
    }
    return render(request, 'pages/settings.html', context)

# Playground
@login_required
def stacked_playground(request):
    return render(request, 'pages/playground/stacked.html')

@login_required
def sidebar_playground(request):
    context = {
        'segment': 'sidebar_playground',
        'parent': 'playground'
    }
    return render(request, 'pages/playground/sidebar.html', context)

# i18n
@login_required
def i18n_view(request):
    context = {
        'segment': 'i18n'
    }
    return render(request, 'pages/i18n.html', context)
