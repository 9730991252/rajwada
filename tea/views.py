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
    
def select_category_items(request, category_id):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            item = []
            for i in Tea_item.objects.filter(status=1, tea_shope_id=e.tea_shope_id):
                selected_status = 0
                if Select_category_item.objects.filter(item_id=i.id,category_id=category_id,status = 1):
                    selected_status = 1 
                print(selected_status)
                item.append({'name':i.name, 'selected_status':selected_status ,'id':i.id})        
        context={
            'e':e,
            'item':item,
            'category':Tea_category.objects.filter(id=category_id).first(),
        }
        return render(request, 'tea/select_category_items.html', context)
    else:
        return redirect('/select_category_items/')
    
def category(request):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        if 'add_category'in request.POST:
            name = request.POST.get('name')
            Tea_category(
                tea_shope_id=e.tea_shope_id,
                name=name,
            ).save()
            return redirect('category')
        if 'edit_category'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            i = Tea_category.objects.filter(id=id).first()
            i.name = name
            i.save()
            return redirect('category')
        if 'active'in request.POST:
            id = request.POST.get('id')
            i = Tea_category.objects.filter(id=id).first()
            i.status = 0
            i.save()
            return redirect('category')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            i = Tea_category.objects.filter(id=id).first()
            i.status = 1
            i.save()
            return redirect('category')
        if 'save_order_by'in request.POST:
            c_id = request.POST.get('id')
            order_by = request.POST.get('order_by')
            c = Tea_category.objects.filter(id=c_id).first()
            c.order_by = order_by
            c.save()
            return redirect('category')        
        context={
            'e':e,
            'category':Tea_category.objects.filter(tea_shope_id=e.tea_shope_id)
        }
        return render(request, 'tea/category.html', context)
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
                qty = OrderDetail.objects.filter(tea_shope_id=e.tea_shope_id,item_id=i.id,date__range=[from_date, to_date] ).aggregate(Sum('qty'))['qty__sum']
                total_price = OrderDetail.objects.filter(tea_shope_id=e.tea_shope_id,item_id=i.id, date__range=[from_date, to_date]).aggregate(Sum('total_price'))['total_price__sum']
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
            'bill':OrderMaster.objects.filter(tea_shope_id=e.tea_shope_id).order_by('-id'),
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
            if Tea_shope.objects.all().exists():
                t = Tea_shope.objects.all().last()
                t.hotel_name = hotel_name
                t.hotel_address = hotel_address
                t.contact_number = mobile
                t.save()
            else:
                Tea_shope(
                    hotel_name = hotel_name,
                    hotel_address = hotel_address,
                    contact_number = mobile, 
                ).save()
        context={
            'e':e ,
            'profile':Tea_shope.objects.all().last(),
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
                tea_shope_id=e.tea_shope_id,
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
            'item':Tea_item.objects.filter(tea_shope_id=e.tea_shope_id),
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
                amount = Cart.objects.filter(employee_id=e.id).aggregate(Sum('total_amount'))
                amount = amount['total_amount__sum']
                order_filter = OrderMaster.objects.filter(tea_shope_id=e.tea_shope_id).count()
                order_filter += 1
                OrderMaster(
                    tea_shope_id=e.tea_shope_id,
                    employee_id = e.id,
                    total_price=amount,
                    order_filter=order_filter
                ).save()
                om = OrderMaster.objects.filter(tea_shope_id=e.tea_shope_id,order_filter=order_filter).first()
                cart = Cart.objects.filter(employee_id=e.id)
                if cart:
                    for c in cart:
                        OrderDetail(
                            employee_id = e.id,
                            tea_shope_id=e.tea_shope_id,
                            item_id=c.item_id,
                            item_name=c.item.name,
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
            'category':Tea_category.objects.filter(status=1).order_by('-order_by'),

        }
        return render(request, 'tea/bill.html', context)
    else:
        return redirect('/login/')
    
def completed_view_bill(request, order_filter):
    if request.session.has_key('tea_mobile'):
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()        
        o = OrderDetail.objects.filter(tea_shope_id=e.tea_shope_id, order_filter=order_filter).aggregate(Sum('total_price'))
        print(e.tea_shope_id)
        
        context={
            'e':e,
            'order_master':OrderMaster.objects.filter(tea_shope_id=e.tea_shope_id, order_filter=order_filter).first(),
            'order_detail':OrderDetail.objects.filter(tea_shope_id=e.tea_shope_id, order_filter=order_filter),
            'tea':e.tea_shope,
            'total_amount':o['total_price__sum'],
            'todayes_total':OrderMaster.objects.filter(ordered_date=date.today(), tea_shope_id=e.tea_shope_id).aggregate(Sum('total_price'))['total_price__sum'],
        }
        return render(request, 'tea/completed_view_bill.html', context)
    else:
        return redirect('/login/')