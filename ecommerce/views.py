from django.shortcuts import render


def home_page(request):
    return render(request,'home.html')

def contactView(request):
    return render(request,'contact.html')

def loginView(request):
    return render(request,'login.html')