from django.shortcuts import render, redirect
from .models import Payment, Income
from .forms import PaymentForm, IncomeForm


def home(request):
    payments = Payment.objects.all()
    listofpayments = []
    for i in payments:
        listofpayments.append(i.listofpayments_set.all())

    context = {'payments': payments, 'listofpayments': listofpayments}
    return render(request, 'home.html', context)


def addPayments(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'BudgetApp/addPayments.html', context)


def addExpense(request):
    form = IncomeForm()
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'BudgetApp/addExpense.html', context)
