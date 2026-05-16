# from django.db import models
# from django.conf import settings


# class Payment(models.Model):

#     class Method(models.TextChoices):
#         PESAPAL = "PESAPAL", "PesaPal"
#         MTN = "MTN", "MTN Mobile Money"
#         AIRTEL = "AIRTEL", "Airtel Pay"
#         BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"

#     class Status(models.TextChoices):
#         PENDING = "PENDING", "Pending"
#         COMPLETED = "COMPLETED", "Completed"
#         FAILED = "FAILED", "Failed"
#         CANCELLED = "CANCELLED", "Cancelled"

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=20, choices=Method.choices)
#     transaction_id = models.CharField(max_length=255, unique=True)
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
#     reference = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.payment_method} - {self.status}"

from django.db import models
from django.conf import settings


class Payment(models.Model):

    class Method(models.TextChoices):
        PESAPAL       = "PESAPAL",       "PesaPal"
        MTN           = "MTN",           "MTN Mobile Money"
        AIRTEL        = "AIRTEL",        "Airtel Pay"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"

    class Status(models.TextChoices):
        PENDING   = "PENDING",   "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED    = "FAILED",    "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Method.choices)
    transaction_id = models.CharField(max_length=255, unique=True)
    status         = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reference      = models.CharField(max_length=255, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.payment_method} - {self.status}"