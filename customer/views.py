from django.shortcuts import render, redirect
from owner.models import * 
# Create your views here.
def customer_scan(request, scan_url):
    bill = Bill.objects.filter(scan_url=scan_url).first()
    if bill:
        context={
            'bill':bill
        }
        return render(request, 'customer/customer_scan.html',context)
    else:
        return redirect('index')
