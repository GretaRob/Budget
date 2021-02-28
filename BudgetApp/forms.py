from django.forms import ModelForm
from .models import Payments, Income


class PaymentForm(ModelForm):
    date_added = forms.DateField(
        initial=today, widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Payments
        fields = "__all__"


class IncomeForm(ModelForm):
    date_added = forms.DateField(
        initial=today, widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Income
        fields = "__all__"
