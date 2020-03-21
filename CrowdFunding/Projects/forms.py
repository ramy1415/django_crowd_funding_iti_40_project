from django import forms
from .models import Category, Tag,Picture
from Users.models import User
import datetime



class AddProject(forms.Form):
    title = forms.CharField(max_length=50, label='Project Title')
    Details = forms.CharField(widget=forms.Textarea)
    Category = forms.ModelChoiceField(queryset=Category.objects.all())
    CurrentMoney = forms.IntegerField(min_value=0)
    TotalTarget = forms.IntegerField(min_value=0)
    Tags = forms. ModelMultipleChoiceField(queryset=Tag.objects.all())
    EndTime = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, datetime.date.today().year+20)))
    Pictures = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # Imageformset = forms.modelformset_factory(Picture,fields='image')
    UserId = forms.ModelChoiceField(queryset=User.objects.all())

