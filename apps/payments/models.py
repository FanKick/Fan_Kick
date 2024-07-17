from django.db import models
from uuid import uuid4

# Create your models here.
class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        READY = "ready", "미결제"
        PAID = "paid", "결제완료"
        CANCELLED = "cancelled", "결제취소"
        FAILED = "failed", "결제실패"
    
    uid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()

    status = models.CharField(
        max_length=9, 
        default=StatusChoices.READY,
        choices=StatusChoices.choices,
        db_index=True
    )

    is_paid = models.BooleanField(default=False, db_index=True)

    @property
    def merchant_uid(self) -> str:
        return self.uid.hex