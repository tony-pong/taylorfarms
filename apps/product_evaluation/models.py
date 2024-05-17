from django.db import models

class ProductEvaluation(models.Model):
    asset_description = models.CharField(max_length=10, blank=False, null=False)
    date = models.DateField()
    result = models.CharField(max_length=4, blank=False, null=False)



    def __str__(self):
        return f"{self.asset_description} - {self.result} on {self.date}"


