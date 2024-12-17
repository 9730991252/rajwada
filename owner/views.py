from django.shortcuts import redirect, render
from .models import *
import random
import string 
# Create your views here.
def owner_home(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        context={
            'o':o
        }
        return render(request, 'owner/owner_home.html', context)
    else:
        return redirect('/login/')
    
def winner(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        context={
            'o':o,
            'lucky_drow':luckydrow_winner.objects.all()
        }
        return render(request, 'owner/winner.html', context)
    else:
        return redirect('/login/')
    
def customer(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        context={
            'o':o,
            'customer':Customer.objects.all()
        }
        return render(request, 'owner/customer.html', context)
    else:
        return redirect('/login/')
    
def lucky_draw(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        context={
            'o':o,
            'participant':participant.objects.filter(status=1)
        }
        return render(request, 'owner/lucky_draw.html', context)
    else:
        return redirect('/login/')
    
def profile(request):
    if request.session.has_key('owner_mobile'):
        m = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=m, status=1).first()
        if request.method == "POST":
            hotel_name = request.POST['hotel_name']
            owner_name = request.POST['owner_name']
            mobile = request.POST['mobile']
            pin = request.POST['pin']
            hotel_address = request.POST['hotel_address']
            Owner(
                id=o.id,
                hotel_name=hotel_name,
                owner_name=owner_name,
                mobile=mobile,
                pin=pin,
                hotel_address=hotel_address
            ).save()
            del request.session['owner_mobile']
            return redirect('login')
        context={
            'o':o
        }
        return render(request, 'owner/profile.html', context)
    else:
        return redirect('/login/')
    
def generate_url():
    count = Bill.objects.all().count()
    count += 1
    url = f'{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{count}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}'
    return url
    

def add_bill(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first() 
        if o:  
            if 'add_bill'in request.POST:
                name = request.POST.get('name')
                amount = request.POST.get('amount')
                person_count = request.POST.get('person_count')
                url = generate_url()
                print(url)
                Bill(
                    name = name,
                    amount = amount,
                    person_count = person_count,
                    scan_url=url
                ).save()
                b = Bill.objects.filter(scan_url=url).first()
                return redirect(f'/owner/view_bill/{b.id}') 
        context={
            'o':o,
            'bill':Bill.objects.all().order_by('-id')
        }
        return render(request, 'owner/add_bill.html', context)
    else:
        return redirect('/login/')
    
def view_bill(request,id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            bill = Bill.objects.filter(id=id).first()
            
        context={
            'o':o,
            'bill':bill
        }
        return render(request, 'owner/view_bill.html', context)
    else:
        return redirect('/login/')