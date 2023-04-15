from django import forms

class ReservationForm(forms.Form):
    item_name = forms.CharField(max_length=255)
    reserved_by = forms.CharField(max_length=255)