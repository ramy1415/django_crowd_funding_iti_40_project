from django.shortcuts import render

def home_page(request):
    return render(request,"Projects/home_page.html")
