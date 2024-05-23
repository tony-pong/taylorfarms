from django.urls import path
from .views import product_evaluation_summary
from .views import product_evaluation_main_page
from .views import product_evaluation_chart

urlpatterns = [
    #path('product-evaluation-summary/', product_evaluation_summary, name='product-evaluation-summary'),
    path('main/', product_evaluation_main_page, name='product_evaluation_main_page'),
    path('api/product-evaluation-summary/', product_evaluation_summary, name='product-evaluation-summary'),
    path('product-evaluation-chart/', product_evaluation_chart, name='product_evaluation_chart'), # for chart
]