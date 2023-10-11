from django.db import models
import uuid

ACCOUNT_STATUS = [('enabled','Enabled'),('disabled','Disabled')]

# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owned_by = models.CharField(max_length=50)
    status = models.CharField(max_length=10,choices=ACCOUNT_STATUS,default='disabled')
    enabled_at = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)
    balance = models.DecimalField(max_digits = 15,decimal_places=2)

    def create(self):
        if not self.balance:
            self.balance = 0
        self.save()
        token = CustAuthToken(user = self)
        token.save()
        return token

    def __str__(self):
        return format(self.id)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_by = models.ForeignKey(Account,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    transaction_time = models.DateTimeField(auto_now=False,auto_now_add=False,null=True)
    status = models.BooleanField(default=True)  # success = 1, failure = 0
    amount = models.DecimalField(max_digits = 15, decimal_places=2)
    reference_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return format(self.id)

class CustAuthToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return format(self.token)

