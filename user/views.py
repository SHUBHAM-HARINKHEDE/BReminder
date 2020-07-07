from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import Birthday,Profile
from django.db.models import Q
import datetime,csv,io 
from django.contrib import messages       
from django.contrib.auth.decorators import login_required  
from .forms import (UserRegisterForm ,
                    UserUpdateForm, 
                    ProfileUpdateForm,
                    BirthdayAddForm
)
# Create your views here.
@login_required 
def index(request):
    today = datetime.date.today()
    #yesterday = today - datetime.timedelta(days = 1)
    #tomorrow = today + datetime.timedelta(days = 1)
    print(today.day,today.month)
    today_birthdays=Birthday.objects.filter(dob__day=today.day,dob__month=today.month)
    criterion1 = Q(dob__day__gt=today.day,dob__month=today.month)
    criterion2 = Q(dob__month__gt=today.month)
    upcomming_birthdays= Birthday.objects.filter(criterion1 & criterion2)
    print("Birthdays\nToday:")
    for b in today_birthdays:
        print(b)
    print("Upcomming birthdays:")
    for b in upcomming_birthdays:
        print(b)


    return HttpResponse("hi")
@login_required 
def home(request):
    today = datetime.date.today()
    nextday = today + datetime.timedelta(days = 1)
    nexr30thday = today + datetime.timedelta(days = 20)
    print(today.day,today.month)
    #today
    today_birthdays=Birthday.objects.filter(dob__day=today.day,dob__month=today.month,user=request.user)
    #upcomming
    criterion1 = Q(dob__day__gt=today.day,dob__month=today.month)
    criterion2 = Q(dob__month__gt=today.month)
    #criterion3 = Q(dob__month__lt=today.month)
    upcomming_birthdays1= Birthday.objects.filter(criterion1).order_by('dob__month','dob__day')
    upcomming_birthdays2=Birthday.objects.filter(criterion2).order_by('dob__month','dob__day')
    upcomming_birthdays3=Birthday.objects.filter(criterion3).order_by('dob__month','dob__day')
    upcomming_birthdays=upcomming_birthdays1 | upcomming_birthdays2 #|upcomming_birthdays3

    print(type(upcomming_birthdays))
    #upcomming_birthdays=Birthday.objects.filter(dob__day__range=[nextday.day,nexr30thday.day],user=request.user)
    recent_birthdays=Birthday.objects.filter(dob__day__lt=today.day,dob__month__lt=today.month,user=request.user)
    print(today_birthdays,upcomming_birthdays)
    context={
        'today_birthdays' : today_birthdays,
        'upcomming_birthdays' : upcomming_birthdays,
        'recent_birthdays' : recent_birthdays
    }
    return render(request,'user/home.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account hs been created! You can login now')
            return redirect('login')
    else:
        form = UserRegisterForm(initial={'email':request.GET.get('email')})
    return render(request, 'user/register.html', {'form':form})

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form,

       }
    
    return render(request,'user/profile.html',context)
def add_birthday(request):
    if request.method == 'POST':
        b_form = BirthdayAddForm(request.POST, instance=request.user)
        
        if b_form.is_valid():
            b_form.save()
            messages.success(request, f'Your Profile has been Updated!')
            return redirect('home')

    else:
        b_form = BirthdayAddForm(instance=request.user)

    context = {
        'form' : b_form,
       }
    
    return render(request,'user/add_birtday.html',context)

def upload_csv(request):
    print('check-1')
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']    # let's check if it is a csv file
            print('check-2')
            data_set = csv_file.read().decode('UTF-8')    # setup a stream which is when we loop through each line we are able to handle a data in a stream
            print('check-3')
            io_string = io.StringIO(data_set)
            print('check-4')
            next(io_string)
            print('check-5')
            for row in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created=Birthday.objects.update_or_create(
                        fname=row[0],
                        mname =row[1],
                        lname=row[2],
                        dob=row[3],
                        user=request.user
                        )       
            messages.success(request, f'birthays has been added.')
        except Exception as e:
            print(e)
            messages.error(request, f'Error occured while adding birthays, please try again!',extra_tags="danger")
    return redirect('add_birthday')
    

