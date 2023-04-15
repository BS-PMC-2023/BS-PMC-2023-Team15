from django import forms
from database.models import Student, Equipment, Reservation
class ReservationForm(forms.Form):
    template_name = "snippets/details_form.html"
    student_id = 123
    item_serial_number = forms.CharField(max_length=100)
    date_from = forms.DateField()
    date_to = forms.DateField()









