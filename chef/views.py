from django.shortcuts import redirect, render
from .models import *
from owner.models import *
from django.contrib import messages
# Create your views here.
def chef_home(request):
    if request.session.has_key('chef_mobile'):
        mobile = request.session['chef_mobile']
        c = Chef.objects.filter(mobile=mobile, status=1).first()
        if 'Accept_item_table'in request.POST:
            table_id = request.POST.get('table_id')
            h = Hotel_cart.objects.filter(table_id=table_id, cook_status='Pendding')
            for h in h:
                hc = Hotel_cart.objects.filter(id=h.id).first()
                hc.cook_status = 'Accepted'
                hc.save()
            return redirect('chef_home')
        if 'Accept_item'in request.POST:
            item_id = request.POST.get('item_id')
            h = Hotel_cart.objects.filter(item_id=item_id, cook_status='Pendding')
            for h in h:
                hc = Hotel_cart.objects.filter(id=h.id).first()
                hc.cook_status = 'Accepted'
                hc.save()
            return redirect('chef_home')
        if 'Accept_item_one'in request.POST:
            id = request.POST.get('id')
            hc = Hotel_cart.objects.filter(id=id).first()
            hc.cook_status = 'Accepted'
            hc.save()
            return redirect('chef_home')
        if 'Delivere'in request.POST:
            item_id = request.POST.get('item_id')
            table_id = request.POST.get('table_id')
            hc = Hotel_cart.objects.filter(item_id=item_id,table_id=table_id).first()
            if hc:
                hc.cook_status = 'Delivered'
                hc.save()
            return redirect('chef_home')
        
        context={
            'c':c,
            'pending_item':Hotel_cart.objects.filter(cook_status='Pendding'),
            'accepted_item':Hotel_cart.objects.filter(cook_status = 'Accepted'),
            'delivered_item': Hotel_cart.objects.filter(cook_status='Delivered')
        }
        return render(request, 'chef/chef_home.html', context)
    else:
        return redirect('/login/')
    