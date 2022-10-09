from django.db import models
from django.db.models import JSONField


CHECK_TYPES = (
    ('kitchen', 'kitchen'),
    ('client', 'client'),
)

STATUS = (
    ('new', 'new'),
    ('rendered', 'rendered'),
    ('printed', 'printed'),
)

class Printer(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=64, unique=True)
    check_type = models.CharField(choices=CHECK_TYPES, max_length=7)
    point_id = models.IntegerField() 
    def __str__(self):
        return f'Printer {self.name} api:{self.api_key}' 
class Check(models.Model):
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(choices=CHECK_TYPES, max_length=7)
    order = JSONField()
    status = models.CharField(choices=STATUS, max_length=8)
    pdf_file = models.FileField()
    def __str__(self):
        return f'{self.printer_id} type: {type}'