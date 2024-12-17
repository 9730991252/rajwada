from django.contrib import messages
from django.shortcuts import render, redirect
from owner.models import * 
# Create your views here.
def customer_scan(request, scan_url):
    bill = Bill.objects.filter(scan_url=scan_url).first()
    if bill:
        if 'add_participants'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')
            customer = Customer.objects.filter(mobile=mobile).first()
            if customer:
                if participant.objects.filter(customer_id=customer.id, bill_id=bill.id).exists():
                    messages.warning(request,f"Participant already Added")   
                else:
                    participant(
                        bill_id=bill.id,
                        customer_id=customer.id,
                    ).save()
                    messages.success(request,f"participant Added Successfuly")   
            else:
                Customer(
                    name=name,
                    mobile=mobile,
                    address=address,
                    ).save()
                customer = Customer.objects.filter(mobile=mobile).first()
                participant(
                    bill_id=bill.id,
                    customer_id=customer.id,
                ).save()
                messages.success(request,f"participant Added Successfuly")   
        participant_id = []
        for p in participant.objects.filter(bill_id=bill.id):
            participant_id.append(p.id)
        luckydrow = ''
        l = luckydrow_winner.objects.filter(winner_participant_id__in = participant_id).last()
        if l:
            luckydrow = l
        print(luckydrow)
        context={
            'bill':bill,
            'participant':participant.objects.filter(bill_id=bill.id),
            'added_person_count':participant.objects.filter(bill_id=bill.id).count(),
            'luckydrow':luckydrow
        }
        return render(request, 'customer/customer_scan.html',context)
    else:
        return redirect('index')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
