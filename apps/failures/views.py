from django.shortcuts import render
from .models import GrossFailure, FailureRecord
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from calendar import month_name
from django.http import JsonResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.db.models.functions import TruncMonth







from django.utils.timezone import make_aware, localtime


#####################Page views

def main_page_view(request):
    # This view will render the main page which includes both the chart and the detailed table.
    return render(request, 'failures/main_page.html')

def failures_snapshot_view(request):
    return render(request, 'failures/snapshots.html')

def detailed_filters_view(request):
    return render(request, 'failures/detailed_filters.html')


def year_over_year_view(request):
    return render(request, 'failures/year_over_year.html')

#####################Chart views

def racing_chart_data(request):
    data_queryset = FailureRecord.objects.annotate(
        month=TruncMonth('date')
    ).values('month', 'item_number_description').annotate(
        count=Count('item_number_description')
    ).order_by('month', '-count')

    data = []
    current_month = None
    current_data = {'yearMonth': '', 'labels': [], 'values': []}  # included 'yearMonth' field
    for record in data_queryset:
        if record['month'] != current_month:
            if current_month is not None:
                data.append(current_data)
                current_data = {'yearMonth': '', 'labels': [], 'values': []}
            current_month = record['month']
            current_data['yearMonth'] = current_month.strftime("%B, %Y")
        current_data['labels'].append(record['item_number_description'])
        current_data['values'].append(record['count'])

    if current_data['labels']:
        data.append(current_data)

    return JsonResponse(data, safe=False)









def chart_data_view(request):
    # Group by 'item_number_description' and count the 'failure_count' for each
    data = GrossFailure.objects.values('item_number_description').annotate(total_failures=Sum('failure_count')).order_by('-total_failures')
    chart_data = {
        'categories': [x['item_number_description'] for x in data],
        'series': [{'name': 'Total Failures', 'data': [x['total_failures'] for x in data]}]
    }
    return JsonResponse(chart_data)




def failure_record_view(request):
    # Fetch distinct values for dropdowns
    usernames = FailureRecord.objects.order_by('user_name').values_list('user_name', flat=True).distinct()
    commodities = FailureRecord.objects.order_by('commodity').values_list('commodity', flat=True).distinct()

    # Start with all records
    records = FailureRecord.objects.all()

    # Retrieve filter values from GET request
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    commodity = request.GET.get('commodity')
    user_name = request.GET.get('user_name')

    # Filter by date range if both start and end dates are provided
    if date_start and date_end:
        records = records.filter(date__range=[date_start, date_end])

    # Filter by commodity if provided
    if commodity:
        records = records.filter(commodity__iexact=commodity)  # Using iexact for case-insensitive exact match

    # Filter by user name if provided
    if user_name:
        records = records.filter(user_name__iexact=user_name)  # Using iexact for case-insensitive exact match
    print(usernames)
    print(commodities)

    return render(request, 'failures/detailed_table.html', {
        'records': records,
        'usernames': usernames,
        'commodities': commodities
    })

def snapshot_shelflife_this_month(request):
    # Get the current month and year
    current_date = datetime.now()

    # Filter records for the current month and year
    records_this_month = FailureRecord.objects.filter(
        date__year=current_date.year,
        date__month=current_date.month
    )

    # Group records by item_number_description and count failures
    grouped_records = records_this_month.values(
        'item_number_description'
    ).annotate(
        failure_count=Count('id')
    ).order_by('-failure_count')[:10]  # Get top 10

    # Extract month name from the current date
    month_name_str = current_date.strftime('%B')

    # Generate the title
    title = f"For the month of {month_name_str} (till date)"

    # Prepare data for the chart
    labels = [record['item_number_description'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    # Data for ApexCharts
    chart_data = {
        'title': title,
        'labels': labels,
        'counts': counts,
    }

    # Render the HTML template with the chart data
    return JsonResponse(chart_data)


def snapshot_shelflife_last_month(request):
    # Get the month for last month
    last_month = datetime.now() - relativedelta(months=1)

    # Filter and annotate records for last month
    records_last_month = FailureRecord.objects.filter(
        date__year=last_month.year,
        date__month=last_month.month
    )

    grouped_records = records_last_month.values(
        'item_number_description'
    ).annotate(failure_count=Count('id')).order_by('-failure_count')[:10]  # Get top 10

    title = f"For the month of {last_month.strftime('%B')} (Previous month)"  # Adjust as needed

    labels = [record['item_number_description'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    chart_data = {'title': title, 'labels': labels, 'counts': counts}
    return JsonResponse(chart_data)




def snapshot_shelflife_two_months_ago(request):
    # Get the month from two months ago
    two_months_ago = datetime.now() - relativedelta(months=2)

    # Filter and annotate records for two months ago
    records_two_months_ago = FailureRecord.objects.filter(
        date__year=two_months_ago.year,
        date__month=two_months_ago.month
    )

    grouped_records = records_two_months_ago.values(
        'item_number_description'
    ).annotate(failure_count=Count('id')).order_by('-failure_count')[:10]  # Get top 10

    title = f"For the month of {two_months_ago.strftime('%B')} (Two months ago)"  # Adjust as needed

    labels = [record['item_number_description'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    chart_data = {'title': title, 'labels': labels, 'counts': counts}
    return JsonResponse(chart_data)


def snapshot_shelflife_this_month_commodities(request):
    # Get the current month and year
    current_date = datetime.now()

    # Filter records for the current month and year
    records_this_month = FailureRecord.objects.filter(
        date__year=current_date.year,
        date__month=current_date.month
    )

    # Group records by commodity and count failures
    grouped_records = records_this_month.values(
        'commodity'
    ).annotate(
        failure_count=Count('id')
    ).order_by('-failure_count')[:10]  # Get top 10

    # Extract month name from the current date
    month_name_str = current_date.strftime('%B')

    # Generate the title
    title = f"For the month of {month_name_str} (till date)"

    # Prepare data for the chart
    labels = [record['commodity'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    # Data for ApexCharts
    chart_data = {
        'title': title,
        'labels': labels,
        'counts': counts,
    }

    # Render the HTML template with the chart data
    return JsonResponse(chart_data)




def ajax_filter_view(request):
    # Fetch distinct values for dropdowns
    commodities = list(FailureRecord.objects.order_by('commodity').values_list('commodity', flat=True).distinct())
    usernames = list(FailureRecord.objects.order_by('user_name').values_list('user_name', flat=True).distinct())
    customers = list(FailureRecord.objects.order_by('customer').values_list('customer', flat=True).distinct())

    # Handle filter inputs
    selected_commodities = request.GET.getlist('commodity')
    selected_usernames = request.GET.getlist('user_name')
    selected_customers = request.GET.getlist('customer')

    # Start with all records
    records = FailureRecord.objects.all()

    # Apply filters based on user input
    if selected_usernames:
        records = records.filter(user_name__in=selected_usernames)
    if selected_commodities:
        records = records.filter(commodity__in=selected_commodities)
    if selected_customers:
        records = records.filter(customer__in=selected_customers)

    # Date filtering logic
    date_start = request.GET.get('date_start', '')
    date_end = request.GET.get('date_end', '')
    if date_start and date_end:
        start_date = datetime.strptime(date_start, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_end, '%Y-%m-%d').date()
        records = records.filter(date__range=[start_date, end_date])

    # Aggregate data and filter where total is more than 50
    #records = records.values('item_number_description').annotate(total=Count('item_number_description')).filter(
    #    total__gt=25).order_by('-total')

    records = records.values('item_number_description').annotate(total=Count('item_number_description')).order_by(
        '-total')

    # Convert QuerySet to a list for JSON serialization
    data = list(records)

    # Fetch the earliest and latest dates for use in filters
    earliest_date = FailureRecord.objects.earliest('date').date
    latest_date = FailureRecord.objects.latest('date').date

    # Return the data as JSON
    return JsonResponse({
        'records': data,
        'commodities': commodities,
        'usernames': usernames,
        'customers': customers,
        'earliest_date': earliest_date.strftime('%Y-%m-%d'),
        'latest_date': latest_date.strftime('%Y-%m-%d')
    })
def snapshot_shelflife_last_month_commodities(request):
    # Get the month for last month
    last_month = datetime.now() - relativedelta(months=1)

    # Filter and annotate records for last month
    records_last_month = FailureRecord.objects.filter(
        date__year=last_month.year,
        date__month=last_month.month
    )

    grouped_records = records_last_month.values(
        'commodity'
    ).annotate(failure_count=Count('id')).order_by('-failure_count')[:10]  # Get top 10

    title = f"For the month of {last_month.strftime('%B')} (Previous month)"  # Adjust as needed

    labels = [record['commodity'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    chart_data = {'title': title, 'labels': labels, 'counts': counts}
    return JsonResponse(chart_data)

def snapshot_shelflife_two_months_ago_commodities(request):
    # Get the month from two months ago
    two_months_ago = datetime.now() - relativedelta(months=2)

    # Filter and annotate records for two months ago
    records_two_months_ago = FailureRecord.objects.filter(
        date__year=two_months_ago.year,
        date__month=two_months_ago.month
    )

    grouped_records = records_two_months_ago.values(
        'commodity'
    ).annotate(failure_count=Count('id')).order_by('-failure_count')[:10]  # Get top 10

    title = f"For the month of {two_months_ago.strftime('%B')} (Two months ago)"  # Adjust as needed

    labels = [record['commodity'] for record in grouped_records]
    counts = [record['failure_count'] for record in grouped_records]

    chart_data = {'title': title, 'labels': labels, 'counts': counts}
    return JsonResponse(chart_data)




def rolling_yoy(request):
    today = datetime.now().date()
    current_month = today.replace(day=1)  # First day of the current month

    # Base query for FailureRecords within the last 24 full months
    start_date = current_month - timedelta(days=365 * 2)
    end_date = current_month - timedelta(days=1)
    base_query = FailureRecord.objects.filter(date__gte=start_date, date__lte=end_date)

    # Annotate each record by month and count total failures per month
    data = base_query.annotate(
        month=TruncMonth('date')
    ).values(
        'month'
    ).annotate(
        total=Count('id')
    ).order_by('month')

    # Prepare the lists of recent and previous data
    month_data = defaultdict(int)
    for entry in data:
        month_data[entry['month'].strftime("%Y-%m-01")] = entry['total']

    recent_data = []
    previous_data = []
    for i in range(24):
        month = current_month - timedelta(days=30 * i)
        month_str = month.strftime("%Y-%m-01")
        if i < 12:
            recent_data.append({'month': month_str, 'total': month_data[month_str]})
        else:
            previous_data.append({'month': month_str, 'total': month_data[month_str]})

    return JsonResponse({
        'recent_data': recent_data,
        'previous_data': previous_data
    })




def rolling_yoy_filtered(request):
    today = datetime.now().date()
    current_month = today.replace(day=1)
    start_date = current_month - timedelta(days=365 * 2)
    end_date = current_month - timedelta(days=1)

    commodities = request.GET.getlist('commodity')  # Get commodities from request
    base_query = FailureRecord.objects.filter(date__gte=start_date, date__lte=end_date)

    # Optionally filter by commodities if they are specified in the GET request
    if commodities:
        base_query = base_query.filter(commodity__in=commodities)

    # Fetch all distinct commodities for the filter dropdown, regardless of current filtering
    all_commodities = FailureRecord.objects.values_list('commodity', flat=True).distinct()

    data = base_query.annotate(month=TruncMonth('date')).values('month').annotate(total=Count('id')).order_by('month')

    month_data = defaultdict(int)
    for entry in data:
        month_data[entry['month'].strftime("%Y-%m-01")] = entry['total']

    recent_data, previous_data = [], []
    for i in range(24):
        month = current_month - timedelta(days=30 * i)
        month_str = month.strftime("%Y-%m-01")
        if i < 12:
            recent_data.append({'month': month_str, 'total': month_data[month_str]})
        else:
            previous_data.append({'month': month_str, 'total': month_data[month_str]})

    # Return both the data for the charts and the list of commodities for the filter
    return JsonResponse({
        'recent_data': recent_data,
        'previous_data': previous_data,
        'commodities': list(all_commodities)  # Convert queryset to list for JSON serialization
    })
