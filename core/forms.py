from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book, Membership, Transaction
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'type', 'serial_number']

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['membership_number', 'duration']
        widgets = {
            'duration': forms.RadioSelect()
        }

class BookSearchForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    serial_number = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError('At least one field must be filled.')
        return cleaned_data

class BookIssueForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'issue_date', 'return_date', 'remarks']
        widgets = {
            'issue_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': timezone.now().strftime('%Y-%m-%dT%H:%M')}),
            'return_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        issue_date = self.cleaned_data.get('issue_date')
        if return_date and issue_date:
            max_return_date = issue_date + timezone.timedelta(days=15)
            if return_date > max_return_date:
                raise forms.ValidationError('Return date cannot be more than 15 days from issue date.')
        return return_date

class BookReturnForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['actual_return_date', 'remarks']
        widgets = {
            'actual_return_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class FinePaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['fine_paid', 'remarks']

    def clean_fine_paid(self):
        fine_paid = self.cleaned_data.get('fine_paid')
        if self.instance.fine_amount > 0 and not fine_paid:
            raise forms.ValidationError('Fine must be paid before proceeding.')
        return fine_paid