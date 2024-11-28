from django.shortcuts import redirect, render
from django.contrib import messages 
from owner.models import *
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('owner_mobile'):
        return redirect('owner_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            o= Owner.objects.filter(mobile=number,pin=pin,status=1)
            if o:
                request.session['owner_mobile'] = request.POST["number"]
                return redirect('owner_home')
    return render(request, 'home/login.html')

def logout(request):
    if request.session.has_key('owner_mobile'):
        del request.session['owner_mobile']
    return redirect('/')