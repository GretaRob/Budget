from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Case, When, Value, CharField
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

    totalpay = Payment.objects.aggregate(tpayments=Sum('cost'))
    totalinc = Income.objects.aggregate(tincome=Sum('amount'))
    totalpayments = round(totalpay['tpayments'], 2)
    totalincome = round(totalinc['tincome'], 2)
    leftmoney = totalincome - totalpayments
    leftmoney = round(leftmoney, 2)

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


def removePayment(request, payment_id):
    paymenttodelete = Payment.objects.get(id=payment_id)
    paymenttodelete.delete()
    return redirect('/')


def removeIncome(request, income_id):
    incometodelete = Income.objects.get(id=income_id)
    incometodelete.delete()
    return redirect('/')


def pie_plot(request):

    # a donut plot showing the spendings per month

    # creating the figure to plot the graph
    fig = Figure()
    # equal aspect ratio ensures that pie is drawn as a circle.
    ax = fig.add_subplot(111, aspect='equal')

    wedges = [Payment.objects.filter(category='rent').aggregate(suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='grocery').aggregate(
                  suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='shopping').aggregate(
                  suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='gym').aggregate(
                  suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='phone').aggregate(
                  suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='freetime').aggregate(
                  suma=Sum('cost'))['suma'] or 0.00,
              Payment.objects.filter(category='other').aggregate(suma=Sum('cost'))['suma'] or 0.00]

    labels = ['rent', 'groceries', 'shopping',
              'gym', 'phone', 'freetime', 'other']

    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 0.0 else ''
    ax.pie(wedges,
           colors=['#ff6666', '#ffcc99', '#99ff99',
                   'grey', '#c2c2f0', '#66b3ff', '#ffb3e6'],
           startangle=90,
           shadow=True,
           autopct=my_autopct,
           pctdistance=0.55)
    ax.legend(wedges, labels=labels, title='Categories',
              loc='center left', bbox_to_anchor=(0.96, 0, 0.5, 1))
    fig.suptitle('Your spending statistics', fontsize=20)

    # draw inner circle for donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # FigureCanvas is the area onto which the figure is drawn
    canvas = FigureCanvas(fig)

    # creating the response as image type jpeg
    response = HttpResponse(content_type="image/jpg")
    canvas.print_jpg(response)

    return response
