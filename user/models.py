from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from user import validators as val
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    mobile = models.CharField(max_length=15, validators=[val.validate_mobile_number],null=True)
    whatsapp_number = models.CharField(max_length=15, validators=[val.validate_mobile_number],null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height >300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Birthday(models.Model):
    fname=models.CharField(max_length=50)
    mname=models.CharField(max_length=50,null=True)
    lname=models.CharField(max_length=50)
    dob=models.DateField(auto_now=False)
    

    def __str__(self):
        return self.fname+self.mname+self.lname

    class Meta:
        managed = True
        verbose_name = 'Birthday'
        verbose_name_plural = 'Birthdays'
