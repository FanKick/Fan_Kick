from django.shortcuts import render

def login(request):
    return render(request, 'base.html')

def nologin(request):
    return render(request, 'nologin_base.html')