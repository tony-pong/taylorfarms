from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    dashboard_view, starter, stacked, sidebar,
    products, users, pricing, maintenance,
    error_404, error_500, settings_view,
    i18n_view, stacked_playground, sidebar_playground, failures_view
)

urlpatterns = [
    path("", login_required(dashboard_view), name="dashboard"),  # Root of the home app
    path("starter/", login_required(starter), name="starter"),
    path('failures/', login_required(failures_view), name='failures'),

    # Layout
    path('layouts/stacked/', login_required(stacked), name="stacked"),
    path('layouts/sidebar/', login_required(sidebar), name="sidebar"),

    # Users
    path('crud/products/', login_required(products), name="products"),
    path('crud/users/', login_required(users), name="users"),

    # Pages
    path('pricing/', login_required(pricing), name="pricing_details"),
    path('maintenance/', login_required(maintenance), name="maintenance"),
    path('404/', login_required(error_404), name="error_404"),
    path('500/', login_required(error_500), name="error_500"),
    path('settings/', login_required(settings_view), name="settings"),
    path('i18n/', login_required(i18n_view), name="i18n_view"),

    # Playground
    path('stacked-playground/', login_required(stacked_playground), name="stacked_playground"),
    path('sidebar-playground/', login_required(sidebar_playground), name="sidebar_playground"),
]
