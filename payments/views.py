from django.shortcuts import render
from .models import Payment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import PaymentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
import pandas as pd
import datetime


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
    return render(request, 'payments/payment_create.html', {'form': form})


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
        pay = Payment.objects.get(id=payment.pk)
        form = PaymentForm(instance=pay)
    return render(request, 'payments/payment_edit.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.user.is_authenticated:
        payment.delete()
        return redirect('payment_list')
    else:
        return redirect('payment_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print(username)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('payment_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def uploadExcel(request):
    if request.method == "GET":
        return render(request, 'payments/uploadExcel.html', {})
    
    if request.method == 'POST' and request.FILES['excel_file']:
        myfile = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print("file name" + filename)
        df = pd.read_excel("media/"+filename)
        
        for index, row in df.iterrows():    
            if pd.isnull(row["Data do Lançamento"]):
                row["Data do Lançamento"] = timezone.now()
            # else:
            #     row["Data do Lançamento"] = datetime.datetime.strptime(row["Data do Lançamento"], '%Y-%m-%d')

            
            if pd.isnull(row["Observações"]):
                row["Observações"]=""

            payment = Payment()
            payment.author = request.user
            payment.title = row["Título"]
            payment.value = row["Valor"]
            payment.publish(publishDate = row["Data do Lançamento"])
            payment.observation = row["Observações"]
            payment.save()

        return redirect('payment_list')



