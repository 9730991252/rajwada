from django.contrib import messages
from django.shortcuts import redirect, render
from owner.models import *
import time
# Create your views here.
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["number"])
        b =int(request.POST["pin"])
        s = a+b
        if s == 11000 :
            request.session['sunil_mobile'] = s
            return redirect('sunil_home')
        else:
            return redirect('sunil_login')
    return render(request, 'home/login.html')



def sunil_home(request):
    if request.session.has_key('sunil_mobile'):
        if 'Add_owner'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            if Owner.objects.filter(mobile=mobile).exists():
                pass
            else:
                Owner(
                    owner_name=name,
                    mobile=mobile,
                    pin=pin
                ).save()
            time.sleep(2)
            return redirect('sunil_home')
        if 'active'in request.POST:
            id = request.POST.get('id')
            o = Owner.objects.filter(id=id).first()
            o.status = 0
            o.save()
            return redirect('sunil_home')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            o = Owner.objects.filter(id=id).first()
            o.status = 1
            o.save()
            return redirect('sunil_home')
        context={
            'owner':Owner.objects.all()
        }
        return render(request, 'sunil/sunil_home.html', context)
    else:
        return redirect('sunil')

