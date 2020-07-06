from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import Birthday,Profile
import datetime 
from django.contrib import messages       
from django.contrib.auth.decorators import login_required  
from .forms import (UserRegisterForm ,
                    UserUpdateForm, 
                    ProfileUpdateForm,
)
# Create your views here.
@login_required 
def index(request):
    today = datetime.date.today()
    #yesterday = today - datetime.timedelta(days = 1)
    #tomorrow = today + datetime.timedelta(days = 1)
    print(today.day,today.month)
    today_birthdays=Birthday.objects.filter(dob__day=today.day,dob__month=today.month)
    upcomming_birthdays=Birthday.objects.filter(dob__day__gt=today.day,dob__month__gt=today.month)
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
    #yesterday = today - datetime.timedelta(days = 1)
    #tomorrow = today + datetime.timedelta(days = 1)
    print(today.day,today.month)
    today_birthdays=Birthday.objects.filter(dob__day=today.day,dob__month=today.month)
    upcomming_birthdays=Birthday.objects.filter(dob__day__gt=today.day,dob__month__gt=today.month)
    recent_birthdays=Birthday.objects.filter(dob__day__lt=today.day,dob__month__lt=today.month)
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


