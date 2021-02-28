from django.forms import ModelForm
from django import forms
from datetime import date
from .models import Payments, Income


class PaymentForm(ModelForm):
    date_added = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day")))

    class Meta:
        model = Payments
        fields = "__all__"


class IncomeForm(ModelForm):
    date_added = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day")))

    class Meta:
        model = Income
        fields = "__all__"
