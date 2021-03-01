from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Case, When, Value, CharField
import calendar
import numpy as np
from .models import Payment, Income
from .forms import PaymentForm, IncomeForm
from django.db.models import Sum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def home(request):
    payments = Payment.objects.all()
    listofpayments = []
    for i in payments:
        listofpayments.append(i)

    allincome = Income.objects.all()
    listofincome = []
    for i in allincome:
        listofincome.append(i)

    totalpayments = Payment.objects.all().aggregate(tpayments=Sum('cost'))
    totalincome = Income.objects.all().aggregate(tincome=Sum('amount'))
    leftmoney = totalincome['tincome'] - totalpayments['tpayments']

    context = {'payments': payments, 'listofpayments': listofpayments,
               'allincome': allincome, 'listofincome': listofincome, 'totalpayments': totalpayments, 'totalincome': totalincome, 'leftmoney': leftmoney}
    return render(request, 'BudgetApp/home.html', context)


def addPayments(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'BudgetApp/addPayments.html', context)


def addIncome(request):
    form = IncomeForm()
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'BudgetApp/addIncome.html', context)


def pie_plot(request):

    # a donut plot showing the spendings per month

    #month_name = calendar.month_name[month]

    # creating the figure to plot the graph
    fig = Figure()
    # equal aspect ratio ensures that pie is drawn as a circle.
    ax = fig.add_subplot(111, aspect='equal')

    labels = []
    wedges = []

    for month in range(1, 13):
        labels.append(month)
        wedges.append(Payment.objects.filter(date_added__month=month).aggregate(
            suma=Sum('cost'))['suma'] or 0.00)

    new_labels = []
    for i in range(1, 13):
        month_name = calendar.month_name[i]
        new_labels.append(
            When(some_datetime_field__month=i, then=Value(month_name)))

    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 0.0 else ''
    ax.pie(wedges,
           colors=['#ff6666', '#ffcc99', '#99ff99',
                   'grey', '#c2c2f0', '#66b3ff', '#ffb3e6'],
           startangle=90,
           shadow=False,
           autopct=my_autopct,
           pctdistance=0.55)
    ax.legend(wedges, labels=new_labels, title='months',
              loc='center left', bbox_to_anchor=(0.96, 0, 0.5, 1))
    fig.suptitle('Your spending statistics per month', fontsize=20)

    # draw inner circle for donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # FigureCanvas is the area onto which the figure is drawn
    canvas = FigureCanvas(fig)

    # creating the response as image type jpeg
    response = HttpResponse(content_type="image/jpg")
    canvas.print_jpg(response)

    return response
