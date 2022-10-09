from django.contrib import admin
from .models import Printer,Check
class PrinterAdmin(admin.ModelAdmin):
    list_filter = ("check_type",)


class CheckAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Check._meta.fields]
    list_filter = ("printer_id", "type", "status")


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
