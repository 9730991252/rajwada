from django.shortcuts import redirect, render
from .models import *
from owner.models import *
# Create your views here.
def waiter_home(request):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Waiter.objects.filter(mobile=mobile, status=1).first()
        print(w)        
        context={
            'w':w,
            'table':Table.objects.all()
        }
        return render(request, 'waiter/waiter_home.html', context)
    else:
        return redirect('/login/')
    
def order(request, tale_id):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Waiter.objects.filter(mobile=mobile, status=1).first()        
        context={
            'w':w,
            'table':Table.objects.all()
        }
        return render(request, 'waiter/order.html', context)
    else:
        return redirect('/login/')
    