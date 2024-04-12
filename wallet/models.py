from django.db import models
from posts.models import Post, Option

from django.conf import settings
User = settings.AUTH_USER_MODEL


class TransactionType(models.TextChoices):
     BET = 'bet', 'Bet'
     TIP = 'tip', 'Tip'
     FEE = 'fee', 'Fee'

class option(models.TextChoices):
     YES = 'yes', 'Yes'
     NO = 'no', 'No'


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=500.00)
    total_spend = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_earn = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    wins = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    losses = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    owner = models.OneToOneField(User, related_name="wallet", on_delete=models.CASCADE, null=True)
 

    @property
    def address(self):
        address = self.owner.username + ".sc"
        return address

    def __str__(self):
        return f"Wallet of {self.owner.username}"


class Bet(models.Model):
    member = models.ForeignKey(
        User, related_name="bet_by", on_delete=models.CASCADE, null=True
    )
    option = models.CharField(
        max_length=50,
        choices=option.choices,
        default=option.YES
    )
    amount = models.IntegerField(default=30)
    post = models.ForeignKey(
        Post, related_name="bet_post", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

class PollBet(models.Model):
    member = models.ForeignKey(
        User, related_name="poll_bet_by", on_delete=models.CASCADE, null=True
    )
    amount = models.IntegerField(default=30)
    option = models.ForeignKey(
        Option, related_name="poll_option", on_delete=models.CASCADE, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)


class Transaction(models.Model):
    transaction_type = models.CharField(
        max_length=50,
        choices=TransactionType.choices,
        default=TransactionType.BET
    )
    sender = models.ForeignKey(
        Wallet, related_name="sender", on_delete=models.CASCADE, null=True
    )
    receiver = models.ForeignKey(
        Wallet, related_name="receiver", on_delete=models.CASCADE, null=True
    )
    amount = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)