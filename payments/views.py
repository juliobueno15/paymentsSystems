from django.shortcuts import render
from .models import Payment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import PaymentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def payment_list(request):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return render(request, 'payments/payment_list.html', {'payments': payments})
    else:
        return render(request, 'payments/index.html')

def payment_detail(request, pk):
    if request.user.is_authenticated:
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_detail.html', {'payment': payment})

def payment_new(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.author = request.user
                payment.publish()
                payment.save()
                return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_edit.html', {'form': form})


def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PaymentForm(request.POST, instance=payment)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.author = request.user
                payment.published_date = timezone.now()
                payment.save()
                return redirect('payment_detail', pk=payment.pk)
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payments/payment_edit.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('payment_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})







