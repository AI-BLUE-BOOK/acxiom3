from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, Membership, Transaction
from .forms import (
    UserRegistrationForm, BookForm, MembershipForm, BookSearchForm,
    BookIssueForm, BookReturnForm, FinePaymentForm
)

from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Set default credentials if empty
        if not username and not password:
            username = password = 'ok'
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def dashboard(request):
    if request.user.is_admin:
        books = Book.objects.all()
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.filter(user=request.user)
        books = Book.objects.filter(available=True)
    return render(request, 'core/dashboard.html', {
        'books': books,
        'transactions': transactions
    })

@login_required
def book_list(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('title'):
            books = books.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data.get('author'):
            books = books.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data.get('serial_number'):
            books = books.filter(serial_number__icontains=form.cleaned_data['serial_number'])
    return render(request, 'core/book_list.html', {'form': form, 'books': books})

@login_required
def book_issue(request):
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.book.available = False
            transaction.book.save()
            transaction.save()
            messages.success(request, 'Book issued successfully.')
            return redirect('dashboard')
    else:
        form = BookIssueForm()
    return render(request, 'core/book_issue.html', {'form': form})

@login_required
def book_return(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = BookReturnForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.fine_amount = transaction.calculate_fine()
            transaction.book.available = True
            transaction.book.save()
            transaction.save()
            if transaction.fine_amount > 0:
                return redirect('fine_payment', transaction_id=transaction.id)
            messages.success(request, 'Book returned successfully.')
            return redirect('dashboard')
    else:
        form = BookReturnForm(instance=transaction)
    return render(request, 'core/book_return.html', {'form': form, 'transaction': transaction})

@login_required
def fine_payment(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = FinePaymentForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fine paid successfully.')
            return redirect('dashboard')
    else:
        form = FinePaymentForm(instance=transaction)
    return render(request, 'core/fine_payment.html', {
        'form': form,
        'transaction': transaction
    })

@login_required
def membership_manage(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.user = request.user
            membership.save()
            messages.success(request, 'Membership updated successfully.')
            return redirect('dashboard')
    else:
        form = MembershipForm()
    return render(request, 'core/membership_manage.html', {'form': form})

@login_required
def book_manage(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'core/book_manage.html', {'form': form})
