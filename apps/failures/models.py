
from django.db import models
from django.http import JsonResponse


#this is the aggregated failures table
class GrossFailure(models.Model):
    item_number_description = models.CharField(max_length=255)
    failure_count = models.IntegerField()
    date_midpoint = models.DateField()
    user_name = models.CharField(max_length=100)
    customer = models.CharField(max_length=30, default='unknown', blank=True, null=False)

    def __str__(self):
        return f"{self.item_number_description} - {self.user_name}"


#this is the individual failure records for flexible pulls
class FailureRecord(models.Model):
    item_number_description = models.CharField(max_length=255)
    date = models.DateField()
    user_name = models.CharField(max_length=100)
    commodity = models.CharField(max_length=255, blank=True, null=True)  # Assuming commodity is stored separately
    customer = models.CharField(max_length=30, default='unknown', blank=True, null=False)

    def __str__(self):
        return f"{self.item_number_description} - {self.user_name} on {self.date}"

#this is the customer sku table
class customerSku(models.Model):
    customer = models.CharField(max_length=30)
    sku = models.CharField(max_length=30)
    product = models.CharField(max_length=150)
    description = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.customer} - {self.sku} - {self.product}"



#
# from .models import FailureRecord
#
# def ajax_filter_view(request):
#     # Get parameters from request
#     user_name = request.GET.get('user_name', None)
#     commodity = request.GET.get('commodity', None)
#     date_start = request.GET.get('date_start', None)
#     date_end = request.GET.get('date_end', None)
#     customer = request.GET.get('customer', None)
#
#     # Start with all records
#     records = FailureRecord.objects.all()
#
#     # Apply filters as necessary
#     if user_name:
#         records = records.filter(user_name=user_name)
#     if commodity:
#         records = records.filter(commodity=commodity)
#     if date_start and date_end:
#         records = records.filter(date__range=[date_start, date_end])
#     if customer:
#         records = records.filter(customer=customer)
#
#     # Format the data for JSON response
#     data = list(records.values('item_number_description', 'date', 'user_name', 'commodity', 'customer'))
#     return JsonResponse({'records': data})
