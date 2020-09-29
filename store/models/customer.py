from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=30, validators=[RegexValidator("^0?[1:9]{1}\d{9}$")])
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    # signup methods
    def isExist_Email(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    def isExist_Phone(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        return False
    # login methods
    @staticmethod
    def getCustomer_by_email(email):
        try:
            return Customer.objects.get(email=email)  # get only single record
        except:
            return False
