from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+201[0|1|2|5][0-9]{8}',
                                 message="Phone number must be entered in the format: '+20[10-11-12-15]-xxxx-xxxx'")
    mobile_phone = models.CharField(validators=[phone_regex], max_length=13, blank=True, null = True)
    profile_pic = models.ImageField(
        upload_to='images/',
        default='images/default_profile.png')
    birth_date = models.DateField(blank=True, null = True)
    fb_profile = models.URLField(blank=True, null = True)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name