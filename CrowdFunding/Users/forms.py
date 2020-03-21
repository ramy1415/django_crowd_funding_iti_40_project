from django import forms
from django.contrib.auth.models import User
from Users.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )
        help_texts = {   # to remove Guides text from forms 
            'username': None,
            'email': None,
        }


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This Email is registered, use another email.')
        return email
#----------------------------------------------------------    
class ProfileForm(forms.ModelForm):
     class Meta():
         model = Profile
         fields = ('mobile_phone','profile_pic')
#----------------------------------------------------------------   
class UpdateUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','first_name','last_name')

class UpdateProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('profile_pic','mobile_phone','birth_date','country','fb_profile')