import csv

from django.contrib import admin, messages
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from .models import Student, Equipment, Reservation, IssueReport,Studio,Category,IssueStatus


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class EquipmentAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith('.csv'):
                self.message_user(request, 'This is not a csv file')
                return redirect("..")

            reader = csv_file.read().decode('UTF-8').split('\n')
            try:
                for r in reader[1:]:
                    if len(r) == 0: break
                    row = r.split(',')
                    _, created = Equipment.objects.update_or_create(
                        serial_number=row[0],
                        category=row[1],
                        brand=row[2],
                        model=row[3],
                        image = row[4],
                        details = row[5]
                    )
            except Exception as e:
                messages.error(request, f"Could not import csv file, or portion of it.")
                return redirect("..")

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_upload.html", payload)




# Register models
admin.site.register(Student)
admin.site.register(Reservation)
admin.site.register(IssueReport)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Studio)
admin.site.register(Category)
admin.site.register(IssueStatus)
