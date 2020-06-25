from django.shortcuts import render
from .models import Payment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import PaymentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import pandas as pd
import datetime
from django.utils.timezone import make_aware


### render payment List (if user is authenticated)
def payment_list(request):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return render(request, 'payments/payment_list.html', {'payments': payments})
    else:
        return render(request, 'payments/index.html')

### render payment detail (if user is authenticated)
def payment_detail(request, pk):
    if request.user.is_authenticated:
        payment = get_object_or_404(Payment, pk=pk)
        return render(request, 'payments/payment_detail.html', {'payment': payment})

### create a new payment,or render create payment page(if user is authenticated)
def payment_new(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PaymentForm(request.POST)
            if form.is_valid():
                #save form into a payment instance
                payment = form.save(commit=False)
                payment.author = request.user
                payment.calculateExternalTax()
                payment.save()
                return redirect('payment_detail', pk=payment.pk)
    else:
        if request.user.is_authenticated:
            form = PaymentForm()
    return render(request, 'payments/payment_create.html', {'form': form})

### edit a existing payment,or render edit payment page(if user is authenticated)
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PaymentForm(request.POST, instance=payment)
            if form.is_valid():
                #save form into a existing payment instance
                payment = form.save(commit=False)
                payment.author = request.user
                payment.calculateExternalTax()
                payment.save()
                return redirect('payment_detail', pk=payment.pk)
    else:
        if request.user.is_authenticated:
            #return to form a payment instance
            form = PaymentForm(instance=payment)
    return render(request, 'payments/payment_edit.html', {'form': form})

### edit a existing payment(if user is authenticated)
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.user.is_authenticated:
        payment.delete()
        return redirect('payment_list')
    else:
        return redirect('payment_list')

### authenticate form fields and register a new user, or render sign up page
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get form fields
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('payment_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


## get a file from request, check if is .xlsx file
def uploadExcel(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'payments/uploadExcel.html', {})
    
    if request.method == 'POST' and request.FILES['excel_file']:
        if request.user.is_authenticated:
            myfile = request.FILES['excel_file']
            fs = FileSystemStorage()
            if myfile.name.endswith(".xlsx"):
                filename = fs.save(myfile.name, myfile)
                df = pd.read_excel("media/"+filename)

                ##iterate over the rows
                for index, row in df.iterrows():
                    if pd.isnull(row["Data do Lançamento"]):
                        row["Data do Lançamento"] = timezone.now()
                    else:
                        row["Data do Lançamento"] = row["Data do Lançamento"].to_pydatetime()
                        #remove warnings from django time zone
                        row["Data do Lançamento"] = make_aware(row["Data do Lançamento"])
        
                    if pd.isnull(row["Observações"]):
                        row["Observações"]=""

                    ##insert row into payment instance
                    payment = Payment()
                    payment.author = request.user
                    payment.title = row["Título"]
                    payment.value = row["Valor"]
                    payment.published_date = row["Data do Lançamento"]
                    payment.calculateExternalTax()
                    payment.observation = row["Observações"]
                    payment.save()
                    

                return redirect('payment_list')
            
            else:
                ##return a message if file inserted is not a .xlsx
                messages.success(request, 'please insert a .xlsx file')
                return render(request, 'payments/uploadExcel.html', {})



