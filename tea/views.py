from django.shortcuts import redirect, render
from .models import *
from django.db.models import Avg, Sum, Min, Max
from django.views.decorators.csrf import csrf_exempt
from datetime import date
# Create your views here.
def tea_home(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()        
        return redirect('bill')
        # context={
        #     'e':e
        # }
        # return render(request, 'tea/tea_home.html', context)
    else:
        return redirect('/login/')
    
def report(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        item = []
        from_date = ''
        to_date = ''
        total_amount = 0
        if 'search_report' in request.POST:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            total_amount = 0
            for i in Tea_item.objects.all():
                qty = OrderDetail.objects.filter(item_id=i.id,date__range=[from_date, to_date] ).aggregate(Sum('qty'))['qty__sum']
                total_price = OrderDetail.objects.filter(item_id=i.id, date__range=[from_date, to_date]).aggregate(Sum('total_price'))['total_price__sum']
                if total_price == None:
                    total_price = 0
                total_amount += total_price
                if qty != None:
                    item.append({'name':i.name, 'qty':qty, 'total_price':total_price})        
        context={
            'e':e,
            'item':item,
            'from_date':from_date,
            'to_date':to_date,
            'total_amount':total_amount,
        }
        return render(request, 'tea/report.html', context)
    else:
        return redirect('/login/')
    
def completed_bill(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'e':e,
            'bill':OrderMaster.objects.all().order_by('-id'),
        }
        return render(request, 'tea/completed_bill.html', context)
    else:
        return redirect('/login/')
    
def profile(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        if request.method == "POST":
            hotel_name = request.POST['hotel_name']
            hotel_address = request.POST['hotel_address']        
            mobile = request.POST['mobile']
            if Tea_profile.objects.all().exists():
                t = Tea_profile.objects.all().last()
                t.hotel_name = hotel_name
                t.hotel_address = hotel_address
                t.contact_number = mobile
                t.save()
            else:
                Tea_profile(
                    hotel_name = hotel_name,
                    hotel_address = hotel_address,
                    contact_number = mobile, 
                ).save()
        context={
            'e':e ,
            'profile':Tea_profile.objects.all().last(),
            'todayes_total':OrderMaster.objects.filter(ordered_date=date.today()).aggregate(Sum('total_price'))['total_price__sum'],

        }
        return render(request, 'tea/profile.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def tea_item(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        if 'add_item'in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')
            Tea_item(
                name=name,
                price=price
            ).save()
            return redirect('tea_item')
        if 'edit_item'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            price = request.POST.get('price')
            c = Tea_item.objects.filter(id=id).first()
            c.name = name
            c.price = price
            c.save()
            return redirect('tea_item')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Tea_item.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('tea_item')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Tea_item.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('tea_item')        
        context={
            'e':e,
            'item':Tea_item.objects.all(),
            'todayes_total':OrderMaster.objects.filter(ordered_date=date.today()).aggregate(Sum('total_price'))['total_price__sum'],        
            }
        return render(request, 'tea/tea_item.html', context)
    else:
        return redirect('/login/')
    
    
@csrf_exempt
def bill(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            amount = Cart.objects.filter(employee_id=e.id).aggregate(Sum('total_amount'))
            amount = amount['total_amount__sum']
            if amount == None:
                amount = 0
            if 'Delete'in request.POST:
                cart_id = request.POST.get('cart_id')
                Cart.objects.filter(id=cart_id).delete()
                return redirect('bill')
            if 'complete_order'in request.POST:
                print('hi')
                amount = Cart.objects.filter(employee_id=e.id).aggregate(Sum('total_amount'))
                amount = amount['total_amount__sum']
                order_filter = OrderMaster.objects.filter().count()
                order_filter += 1
                OrderMaster(
                    employee_id = e.id,
                    total_price=amount,
                    order_filter=order_filter
                ).save()
                om = OrderMaster.objects.filter(order_filter=order_filter).first()
                cart = Cart.objects.filter(employee_id=e.id)
                if cart:
                    for c in cart:
                        OrderDetail(
                            employee_id = e.id,
                            item_id=c.item_id,
                            qty=c.qty,
                            price=c.price,
                            total_price=c.total_amount,
                            order_filter=order_filter,
                        ).save()
                Cart.objects.filter(employee_id=e.id).delete()
                return redirect(f'/tea/completed_view_bill/{order_filter}')
        context={
            'e':e,
            'cart':Cart.objects.filter(employee_id=e.id),
            'item':Tea_item.objects.filter(status=1),
            'amount':amount,
            'todayes_total':OrderMaster.objects.filter(ordered_date=date.today()).aggregate(Sum('total_price'))['total_price__sum'],
        }
        return render(request, 'tea/bill.html', context)
    else:
        return redirect('/login/')
    
def completed_view_bill(request, order_filter):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()        
        o = OrderDetail.objects.filter(order_filter=order_filter).aggregate(Sum('total_price'))
        
        context={
            'e':e,
            'order_master':OrderMaster.objects.filter(order_filter=order_filter).first(),
            'order_detail':OrderDetail.objects.filter(order_filter=order_filter),
            'tea':Tea_profile.objects.all().first(),
            'total_amount':o['total_price__sum'],
            'todayes_total':OrderMaster.objects.filter(ordered_date=date.today()).aggregate(Sum('total_price'))['total_price__sum'],
        }
        return render(request, 'tea/completed_view_bill.html', context)
    else:
        return redirect('/login/')