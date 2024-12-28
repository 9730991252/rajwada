from django.shortcuts import redirect, render
from .models import *
from owner.models import *
# Create your views here.
def waiter_home(request):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Waiter.objects.filter(mobile=mobile, status=1).first()
        table = []
        runing_table = []
        for t in Table.objects.filter(status=1):
            status = 'no'        
            c = Hotel_cart.objects.filter(table_id=t.id).exists()
            if c:
                runing_table.append({'id':t.id,'table_number':t.table_number})
                status = 'yes'        
            table.append({'id':t.id,'table_number':t.table_number,'status':status})
        context={
            'w':w,
            'table':table,
            'runing_table':runing_table
        }
        return render(request, 'waiter/waiter_home.html', context)
    else:
        return redirect('/login/')
    
def order(request, table_id):
    if request.session.has_key('waiter_mobile'):
        mobile = request.session['waiter_mobile']
        w = Waiter.objects.filter(mobile=mobile, status=1).first()
        if 'Delete'in request.POST:
            cart_id = request.POST.get('cart_id')
            Hotel_cart.objects.filter(id=cart_id).delete()
            return redirect(f'/waiter/order/{table_id}') 
        
               
        context={
            'w':w,
            'table':Table.objects.get(id=table_id),
            'category':Category.objects.filter(status=1),
            'cart':Hotel_cart.objects.filter(table_id=table_id),
            'table_id':table_id
        }
        return render(request, 'waiter/order.html', context)
    else:
        return redirect('/login/')
    