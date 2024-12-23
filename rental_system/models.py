from django.db import models
from datetime import date

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=220)
    address = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    is_vacant = models.BooleanField(default=False)
    image = models.ImageField(upload_to='property_images/')
    area = models.CharField(max_length=100)
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    garages = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Tenant(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True, related_name='tenants')
    rent_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    move_in_date = models.DateField()
    move_out_date = models.DateField(null=True, blank=True)

    def calculate_debts(self):
        """Calculate any outstanding payments."""
        total_due = Payment.objects.filter(tenant=self, status='due').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_due

    def __str__(self):
        return self.name


class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name='payments', on_delete=models.CASCADE)
    month = models.DateField()  # Represents the first day of the month for payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[('mpesa', 'M-Pesa'), ('cash', 'Cash')])
    status = models.CharField(
        max_length=20,
        choices=[('paid', 'Paid'), ('due', 'Due'), ('new', 'New')],
        default='new'
    )
    description = models.CharField(max_length=255, blank=True)  # e.g., "First Rent", "Deposit"

    def update_status(self):
        """Update payment status based on current date and payment."""
        if self.payment_date:
            self.status = 'paid'
        elif self.month < date.today().replace(day=1):
            self.status = 'due'
        else:
            self.status = 'new'
        self.save()

    def __str__(self):
        return f"{self.tenant.name} - {self.month.strftime('%B %Y')} - {self.status}"
