"""Budget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BudgetApp.views import home, addPayments, addIncome, removePayment, removeIncome, pie_plot
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('addPayments/', addPayments, name='addPayments'),
    path('addIncome/', addIncome, name='addIncome'),
    path('removePayment/<int:payment_id>', removePayment, name='removePayment'),
    path('removeIncome/<int:income_id>', removeIncome, name='removeIncome'),
    path('pie_plot/', pie_plot, name='pie_plot'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
