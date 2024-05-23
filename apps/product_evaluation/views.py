

from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Avg, FloatField
from django.db.models.functions import Cast
from .models import ProductEvaluation
from django.utils.timezone import make_aware




# renders the main_page html


def product_evaluation_main_page(request):
    return render(request, 'main_page.html')

# helper function for main product_evaluation_summary function
def calc_fail_percentage(data):
    total_count = data.count()
    fail_count = data.filter(result__iexact='fail').count()
    fail_percentage = (fail_count / total_count) * 100 if total_count > 0 else 0
    return round(fail_percentage, 2)

def product_evaluation_summary(request):
    # Get all the data from the ProductEvaluation model
    data = ProductEvaluation.objects.all()

    # Get the unique assets
    unique_assets = data.values_list('asset_description', flat=True).distinct()

    # Calculate the most recent date sampled and fail percentage for each asset and time period
    asset_stats = []
    for asset in unique_assets:
        asset_data = data.filter(asset_description=asset)
        if not asset_data.exists():
            asset_stats.append({
                'asset': asset,
                'most_recent_date_sampled': 'No sample data',
                'pass_count': 0,
                'fail_count': 0,
                'daily_fail': '0.00%',
                'week_range': 'No data',
                'week_fail': '0.00%',
                'month_range': 'No data',
                'month_fail': '0.00%',
                'ytd_range': 'No data',
                'ytd_fail': '0.00%',
                'prev_year_range': 'No data',
                'prev_year_fail': '0.00%'
            })
        else:
            max_date = asset_data.latest('date').date
            daily_fail = calc_fail_percentage(asset_data.filter(date=max_date))
            week_start = max_date - timedelta(days=max_date.weekday())
            week_fail = calc_fail_percentage(asset_data.filter(date__gte=week_start, date__lte=max_date))
            month_start = datetime(max_date.year, max_date.month, 1)
            month_fail = calc_fail_percentage(asset_data.filter(date__gte=month_start, date__lte=max_date))
            year_start = datetime(max_date.year, 1, 1)
            ytd_fail = calc_fail_percentage(asset_data.filter(date__gte=year_start, date__lte=max_date))
            prev_year_max_date = max_date.replace(year=max_date.year - 1)
            prev_year_start = datetime(prev_year_max_date.year, 1, 1)
            prev_year_fail = calc_fail_percentage(asset_data.filter(date__gte=prev_year_start, date__lte=prev_year_max_date))
            pass_count = asset_data.filter(date=max_date, result__iexact='pass').count()
            fail_count = asset_data.filter(date=max_date, result__iexact='fail').count()
            asset_stats.append({
                'asset': asset,
                'most_recent_date_sampled': max_date.strftime('%Y-%m-%d'),
                'pass_count': pass_count,
                'fail_count': fail_count,
                'daily_fail': f"{daily_fail:.2f}%",
                'week_range': f"{week_start.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}",
                'week_fail': f"{week_fail:.2f}%",
                'month_range': f"{month_start.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}",
                'month_fail': f"{month_fail:.2f}%",
                'ytd_range': f"{year_start.strftime('%Y')} to {max_date.strftime('%Y')}",
                'ytd_fail': f"{ytd_fail:.2f}%",
                'prev_year_range': f"{prev_year_start.strftime('%Y')} to {prev_year_max_date.strftime('%Y')}",
                'prev_year_fail': f"{prev_year_fail:.2f}%"
            })

    # Add an "Overall" row at the top
    max_date = data.latest('date').date
    overall_pass_count = data.filter(date=max_date, result__iexact='pass').count()
    overall_fail_count = data.filter(date=max_date, result__iexact='fail').count()
    week_start = max_date - timedelta(days=max_date.weekday())
    month_start = datetime(max_date.year, max_date.month, 1)
    year_start = datetime(max_date.year, 1, 1)
    prev_year_max_date = max_date.replace(year=max_date.year - 1)
    prev_year_start = datetime(prev_year_max_date.year, 1, 1)

    overall_row = {
        'asset': 'Overall',
        'most_recent_date_sampled': max_date.strftime('%Y-%m-%d'),
        'pass_count': overall_pass_count,
        'fail_count': overall_fail_count,
        'daily_fail': f"{calc_fail_percentage(data.filter(date=max_date)):.2f}%",
        'week_range': f"{week_start.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}",
        'week_fail': f"{calc_fail_percentage(data.filter(date__gte=week_start, date__lte=max_date)):.2f}%",
        'month_range': f"{month_start.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}",
        'month_fail': f"{calc_fail_percentage(data.filter(date__gte=month_start, date__lte=max_date)):.2f}%",
        'ytd_range': f"{year_start.strftime('%Y')} to {max_date.strftime('%Y')}",
        'ytd_fail': f"{calc_fail_percentage(data.filter(date__gte=year_start, date__lte=max_date)):.2f}%",
        'prev_year_range': f"{prev_year_start.strftime('%Y')} to {prev_year_max_date.strftime('%Y')}",
        'prev_year_fail': f"{calc_fail_percentage(data.filter(date__gte=prev_year_start, date__lte=prev_year_max_date)):.2f}%"
    }

    # Combine the overall row with the asset stats
    summary_data = [overall_row] + asset_stats

    return JsonResponse(summary_data, safe=False)




##### for monthly plot

import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils.timezone import make_aware, is_naive
from .models import ProductEvaluation

def make_aware_if_naive(dt):
    return make_aware(dt) if is_naive(dt) else dt

def get_monthly_fail_percentages():
    now = datetime.now()
    first_day_of_current_month = make_aware_if_naive(now.replace(day=1))
    last_day_of_current_month = make_aware_if_naive((first_day_of_current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1))
    first_day_of_last_12_months = first_day_of_current_month - timedelta(days=365)

    # Generate the last 12 months
    months = [(first_day_of_current_month - timedelta(days=i*30)).strftime('%Y-%m') for i in range(12)]
    months = sorted(list(set(months)), reverse=True)  # Ensure uniqueness and order, most recent first

    fail_percentages = {}

    # Get all distinct asset descriptions
    asset_descriptions = ProductEvaluation.objects.values_list('asset_description', flat=True).distinct()

    for asset in asset_descriptions:
        asset_data = ProductEvaluation.objects.filter(
            asset_description=asset,
            date__gte=first_day_of_last_12_months,
            date__lte=last_day_of_current_month
        ).annotate(month=TruncMonth('date')).values('month').annotate(
            total=Count('id'),
            fails=Count('id', filter=Q(result='Fail'))
        ).order_by('month')

        monthly_data = {month['month'].strftime('%Y-%m'): (month['fails'] / month['total']) * 100 for month in asset_data}

        fail_percentages[asset] = [
            {'month': month, 'fail_percentage': round(monthly_data.get(month, 0), 2)}
            for month in months
        ]

    # Remove asset descriptions with all zero values
    filtered_fail_percentages = {
        asset: data for asset, data in fail_percentages.items()
        if any(item['fail_percentage'] > 0 for item in data)
    }

    return filtered_fail_percentages

def product_evaluation_chart(request):
    data = get_monthly_fail_percentages()
    return JsonResponse(data, safe=False)
