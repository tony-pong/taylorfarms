from django.urls import path
from . import views

urlpatterns = [
    path('', views.failures_snapshot_view, name='snapshot'),  # Default view set to snapshot
    path('main-page/', views.main_page_view, name='main_page'),
    path('year-over-year/', views.year_over_year_view, name='year_over_year'),
    path('rolling-yoy-data-filtered/', views.rolling_yoy_filtered, name='rolling-yoy-data-filtered'),
    path('racing-chart-data/', views.racing_chart_data, name='racing_chart_data'),  # URL pattern for the racing chart data
    path('rolling-yoy-data/', views.rolling_yoy, name='rolling_yoy_data'), # api endpoint for rolling yoy
    path('chart-data/', views.chart_data_view, name='chart_data'),
    path('failure-records/', views.failure_record_view, name='failure_records'),
    path('ajax-filter-data/', views.ajax_filter_view, name='ajax_filter_data'),
    path('snapshot-shelflife-this-month/', views.snapshot_shelflife_this_month, name='snapshot_shelflife_this_month'),
    path('snapshot-shelflife-last-month/', views.snapshot_shelflife_last_month, name='snapshot_shelflife_last_month'),
    path('snapshot-shelflife-two-months-ago/', views.snapshot_shelflife_two_months_ago, name='snapshot_shelflife_two_months_ago'),
    # New paths for commodities
    path('snapshot-shelflife-this-month-commodities/', views.snapshot_shelflife_this_month_commodities, name='snapshot_shelflife_this_month_commodities'),
    path('snapshot-shelflife-last-month-commodities/', views.snapshot_shelflife_last_month_commodities, name='snapshot_shelflife_last_month_commodities'),
    path('snapshot-shelflife-two-months-ago-commodities/', views.snapshot_shelflife_two_months_ago_commodities, name='snapshot_shelflife_two_months_ago_commodities'),
    #New path for detailed fitler view
    path('detailed-filters/', views.detailed_filters_view, name='detailed_filters'),

]
