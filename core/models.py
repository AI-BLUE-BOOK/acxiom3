from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

class Book(models.Model):
    TYPES = [
        ('BOOK', 'Book'),
        ('MOVIE', 'Movie')
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    type = models.CharField(max_length=5, choices=TYPES, default='BOOK')
    serial_number = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Membership(models.Model):
    DURATIONS = [
        (6, '6 Months'),
        (12, '1 Year'),
        (24, '2 Years')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(choices=DURATIONS, default=6)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Membership {self.membership_number} - {self.user.username}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField()
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fine_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def calculate_fine(self):
        if not self.actual_return_date:
            return 0
        if self.actual_return_date > self.return_date:
            days_late = (self.actual_return_date - self.return_date).days
            return days_late * 1.0  # $1 per day
        return 0
