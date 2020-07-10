"""BirtdayReminder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#to access media files on browswer
from django.conf import settings
from django.conf.urls.static import static
#Authentication
from django.contrib.auth import views as auth_views 
#user views
from user import views as user_views
from user.views import BirthdayDeleteView
urlpatterns = [
    path('admin/', admin.site.urls),
    #login
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html',redirect_authenticated_user=True), name='login'),
    #logout
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    #register
    path('register/', user_views.register , name='register'),
    #forgot password
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset.html'
        ),
        name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html'
        ),
        name='password_reset_confirm'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
        ),
        name='password_reset_done'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
        ),
        name='password_reset_complete'),
    #change password  
    path('password-change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='user/password_change.html'
        ),
        name='password_change'),  
    path('password-change-done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='user/password_change_done.html'
        ),
        name='password_change_done'),
    
    path('profile/', user_views.profile , name='profile'),
    path('home/', user_views.home , name='home'),
    path('add_birtday/', user_views.add_birthday , name='add_birthday'),
    path('home/upload_csv', user_views.upload_csv , name='upload_csv'),
    path('about/',user_views.about,name='about'),
    path('contact/',user_views.contact,name='contact'),
    path('birthday/<int:pk>/delete/', BirthdayDeleteView.as_view(), name='birthday-delete'),
    path('delete_user/', user_views.delete_user_profile , name='delete_user'),
    path('',user_views.index,name="index"),
]
#to access media files on browswer
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)