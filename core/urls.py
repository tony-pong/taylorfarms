"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.views.static import serve

# Import SignInView from your users app
from apps.users.views import SignInView
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    # Redirect root to login view
  # path('', LoginView.as_view(), name='account_login'),
    path('', SignInView.as_view(), name='signin_root'),

    path("admin/", admin.site.urls),
    path("failures/", include('apps.failures.urls')),  # shelf life failures app
    path('product-evaluation/', include('apps.product_evaluation.urls')),  # product evaluation app
    path("api/", include("apps.api.urls")),
    path("users/", include("apps.users.urls")),
    path("charts/", include("apps.charts.urls")),
    path("tables/", include("apps.tables.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path('cms/', include('apps.cms.urls')),
    path('payments/', include('apps.payments.urls')),
    path('accounts/', include('allauth.urls')),  # Keep this for handling other auth views

    # Previously configured apps might conflict with the new root path; be sure to adjust as necessary
    path("home/", include("home.urls")),
    path('files/', include('apps.file_manager.urls')),

    path('cms-admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),

    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/'      , SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("__debug__/", include("debug_toolbar.urls")),

    path('sentry-debug/', trigger_error),
    path('i18n/', include('django.conf.urls.i18n')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

urlpatterns += static(settings.CELERY_LOGS_URL, document_root=settings.CELERY_LOGS_DIR)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL      , document_root=settings.MEDIA_ROOT     )
