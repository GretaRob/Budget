from django.db import models


CHOICES = (
    ('rent', 'Rent'),
    ('groceries', 'Groceries'),
    ('shopping', 'Shopping'),
    ('gym', 'Gym'),
    ('phone', 'Phone'),
    ('freetime', 'Freetime'),
    ('other', 'Other')
)

# what have you spent


class Payment(models.Model):
    payment_name = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField()
    cost = models.FloatField()
    category = models.CharField(
        max_length=25, choices=CHOICES, default='other')

    def __str__(self):
        return str(self.payment_name)

# what have you earned


class Income(models.Model):
    income_name = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.income_name)
