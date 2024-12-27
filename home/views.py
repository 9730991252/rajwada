from django.shortcuts import redirect, render
from django.contrib import messages 
from owner.models import *
from waiter.models import *
from chef.models import *
from tea.models import *
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def menu(request):
    return render(request, 'home/menu.html')

def login(request):
    if request.session.has_key('owner_mobile'):
        return redirect('owner_home')
    
    if request.session.has_key('waiter_mobile'):
        return redirect('waiter_home')
    if request.session.has_key('chef_mobile'):
        return redirect('chef_home')
    if request.session.has_key('tea_mobile'):
        return redirect('tea_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            o= Owner.objects.filter(mobile=number,pin=pin,status=1)
            if o:
                request.session['owner_mobile'] = request.POST["number"]
                return redirect('owner_home')
            w= Waiter.objects.filter(mobile=number,pin=pin,status=1)
            if w:
                request.session['waiter_mobile'] = request.POST["number"]
                return redirect('waiter_home')
            c= Chef.objects.filter(mobile=number,pin=pin,status=1)
            if c:
                request.session['chef_mobile'] = request.POST["number"]
                return redirect('chef_home')
            t= Tea_employee.objects.filter(mobile=number,pin=pin,status=1)
            if t:
                request.session['tea_mobile'] = request.POST["number"]
                return redirect('tea_home')
    return render(request, 'home/login.html')

def logout(request):
    if request.session.has_key('owner_mobile'):
        del request.session['owner_mobile']
    if request.session.has_key('waiter_mobile'):
        del request.session['waiter_mobile']
    if request.session.has_key('chef_mobile'):
        del request.session['chef_mobile']
    if request.session.has_key('tea_mobile'):
        del request.session['tea_mobile']
    return redirect('/')