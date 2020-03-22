from django import forms
from django.forms import ModelForm
from .models import Project, Category, Tag, Picture,Donation
from Users.models import User
import datetime


class AddProject(forms.Form):
    title = forms.CharField(max_length=50, label='Project Title')
    Details = forms.CharField(widget=forms.Textarea)
    Category = forms.ModelChoiceField(queryset=Category.objects.all())
    CurrentMoney = forms.IntegerField(min_value=0, label='Current money')
    TotalTarget = forms.IntegerField(min_value=0, label="Total Target")
    Tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    EndTime = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, datetime.date.today().year + 20)),
                              label='End Time')
    Pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    UserId = forms.ModelChoiceField(queryset=User.objects.all(), )


class EditProject(ModelForm):
    class Meta:
        model = Project
        exclude = ('start_time', 'user_id',)
        widgets = {
            'end_time': forms.SelectDateWidget(years=range(2020, datetime.date.today().year + 20)),
        }


# class DonationForm(ModelForm):
#     class Meta:
#         model = Donation
#         fields = (amount,)
