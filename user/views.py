from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import Birthday,Profile,Contact
from django.db.models import Q
import datetime,csv,io,os
from django.contrib import messages       
from django.contrib.auth.decorators import login_required  
from .forms import (UserRegisterForm ,
                    UserUpdateForm, 
                    ProfileUpdateForm,
                    BirthdayAddForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView, DetailView
from django.core.mail import send_mail
#to check password
from django.contrib.auth.hashers import check_password
#to get back to previous page
from django.urls import reverse


# views

def index(request):
    return render(request,'user/index.html')

def handler404(request, exception):
    return render(request,'user/404.html')
def handler500(request, *args, **argv):
    return render(request,'user/500.html',status=500)

@login_required 
def home(request,*args):
    today = datetime.date.today()
    print(today.day,today.month)
    #today
    today_birthdays=Birthday.objects.filter(dob__day=today.day,dob__month=today.month,user=request.user)
    #upcomming
    criterion1 = Q(dob__day__gt=today.day,dob__month=today.month,user=request.user)
    criterion2 = Q(dob__month__gt=today.month,user=request.user)
    #criterion3 = Q(dob__month__lt=today.month)
    upcomming_birthdays1= Birthday.objects.filter(criterion1).order_by('dob__month','dob__day')
    upcomming_birthdays2=Birthday.objects.filter(criterion2).order_by('dob__month','dob__day')
    #upcomming_birthdays3=Birthday.objects.filter(criterion3).order_by('dob__month','dob__day')
    upcomming_birthdays=upcomming_birthdays1 | upcomming_birthdays2 #|upcomming_birthdays3

    print(type(upcomming_birthdays))
    #upcomming_birthdays=Birthday.objects.filter(dob__day__range=[nextday.day,nexr30thday.day],user=request.user)
    recent_birthdays1=Birthday.objects.filter(dob__day__lt=today.day,dob__month=today.month,user=request.user).order_by('-dob__month','-dob__day')
    recent_birthdays2=Birthday.objects.filter(dob__month__lt=today.month,user=request.user).order_by('-dob__month','-dob__day')
    recent_birthdays=recent_birthdays1 | recent_birthdays2
    #all birthday for specific user
    all_birthdays=Birthday.objects.filter(user=request.user).order_by('dob__month','dob__day')
    context={
        'today_birthdays' : today_birthdays,
        'upcomming_birthdays' : upcomming_birthdays,
        'recent_birthdays' : recent_birthdays,
        'all_birthdays' : all_birthdays
    }
    return render(request,'user/home.html',context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
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

@login_required 
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

@login_required 
def add_birthday(request):
    
    if request.method == 'POST':
        b_form = BirthdayAddForm(request.POST)
        b_form.user=request.user
        
        if b_form.is_valid():
            bd = b_form.save(commit=False)
            bd.user = request.user
            bd.save()
            messages.success(request, f'Birthday has been added successfuly.')

    else:
        b_form = BirthdayAddForm(instance=request.user)

    context = {
        'form' : b_form,
       }
    
    return render(request,'user/add_birtday.html',context)

@login_required 
def upload_csv(request):
    print('check-1')
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']    # let's check if it is a csv file
            data_set = csv_file.read().decode('UTF-8')    # setup a stream which is when we loop through each line we are able to handle a data in a stream
            io_string = io.StringIO(data_set)
            next(io_string)
            for row in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created=Birthday.objects.update_or_create(
                        fname=row[0],
                        mname =row[1],
                        lname=row[2],
                        dob=row[3],
                        mobile=row[4],
                        whatsapp_number=row[5],
                        email=row[6],
                        user=request.user
                        )       
            messages.success(request, f'birthays has been added.')
        except Exception as e:
            print(e)
            messages.error(request, f'Error occured while adding birthays, please try again!',extra_tags="danger")
    return redirect('add_birthday')
    

def about(request):
    return render(request,'user/about.html')

def contact(request):
    
    if request.method == 'POST':   
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contact=Contact()
        contact.name=name
        contact.email=email
        contact.subject=subject
        contact.message=message
        contact.save()     
        message="Hello,\n"+message+"\nRegards,\n"+name+"\n"+email
        try:
            send_mail(
            subject,
            message,
            email,
            [os.environ.get('EMAIL_HOST_USER')],
            fail_silently=False,
            )
            messages.success(request, f'We have recieved your query,we will come back to you soon..')
        except Exception as e:
            print(e)
            messages.error(request, f'Something went wrong!')
    return render(request,'user/contact.html')
    
@login_required
def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['First Name','Middle Name','Last Name','DOB'])

    for birthday in Birthday.objects.filter(user=request.user).order_by('dob__month','dob__day'):
        writer.writerow([birthday.fname,birthday.mname,birthday.lname,birthday.dob])

    response['Content-Disposition'] = 'attachment; filename="birthday.csv"'
    
    return response

@login_required
def delete_user_profile(request):
    if request.method == 'POST':
        if check_password(request.POST.get('password'),request.user.password):   
            request.user.delete()
            return render(request,'user/delete_profile_done.html')
        else:
            messages.error(request,"Please enter correct password to procced!",)
    return render(request,'user/delete_profile.html')

@login_required
def delete_user_birthdays(request):
    if Birthday.objects.filter(user=request.user).delete() :
        messages.success(request,"All birthdays are deleted!",)
    else:
        messages.error(request,"Failed to delete birthdays!",)
    return redirect('home')
    

class BirthdayDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Birthday
    success_url = '/home/#all'
    success_message = "Birthday was deleted successfully."

    def test_func(self):
        birthday = self.get_object()
        if self.request.user == birthday.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BirthdayDeleteView, self).delete(request, *args, **kwargs)

class BirthdayUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Birthday
    fields = ['fname','mname','lname','dob','mobile','whatsapp_number','email']
    
    
    def form_valid(self,form):
        form.instance.user =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        birtday = self.get_object()
        if self.request.user == birtday.user:
            return True
        return False
    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))

class BirthdayDetailView(DetailView):
    model = Birthday
    #<app>/<model>_<viewtype>.html






