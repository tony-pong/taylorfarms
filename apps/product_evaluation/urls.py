from django.urls import path
from .views import product_evaluation_summary

urlpatterns = [
    #path('product-evaluation-summary/', product_evaluation_summary, name='product-evaluation-summary'),
    path('api/product-evaluation-summary/', product_evaluation_summary, name='product-evaluation-summary'),
]