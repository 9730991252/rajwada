from django.shortcuts import redirect, render
from .models import *
import random
import string
from waiter.models import * 
from chef.models import * 
from tea.models import * 
from django.db.models import Avg, Sum, Min, Max
from django.views.decorators.csrf import csrf_exempt
import math

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
    
def tea_employee(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        if 'add_tea_employee'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            Tea_employee(
                name=name,
                mobile = mobile,
                pin = pin,
            ).save()
            return redirect('tea_employee')
        if 'edit_tea_employee'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            w = Tea_employee.objects.filter(id=id).first()
            w.name = name
            w.mobile = mobile
            w.pin = pin
            w.save()
            return redirect('tea_employee')
        if 'active'in request.POST:
            id = request.POST.get('id')
            w = Tea_employee.objects.filter(id=id).first()
            w.status = 0
            w.save()
            return redirect('tea_employee')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            w = Tea_employee.objects.filter(id=id).first()
            w.status = 1
            w.save()        
        context={
            'o':o,
            'tea_employee':Tea_employee.objects.all()
        }
        return render(request, 'owner/tea_employee.html', context)
    else:
        return redirect('/login/')
    
def running_table(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        table = []
        runing_table = []
        for t in Table.objects.filter(status=1):
            status = 'no'        
            c = Hotel_cart.objects.filter(table_id=t.id).exists()
            if c:
                runing_table.append({'id':t.id,'table_number':t.table_number})
                status = 'yes'        
            table.append({'id':t.id,'table_number':t.table_number,'status':status})
        if 'chang_paid_status'in request.POST:
            bill_id = request.POST.get('bill_id')
            b = Hotel_order_Master.objects.filter(id=bill_id).first()
            b.paid_status = 1
            b.save()
        context={
            'o':o,
            'table':table,
            'runing_table':runing_table,
            'unpaid_bills':Hotel_order_Master.objects.filter(paid_status=0).order_by('-id')[0:10]
        }
        return render(request, 'owner/running_table.html', context)
    else:
        return redirect('/login/')
    
def table(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        if 'add_table'in request.POST:
            table_number = Table.objects.all().count()
            table_number += 1
            Table(
                table_number=table_number
            ).save()
            return redirect('table')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Table.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('table')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Table.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('table')
        
        context={
            'o':o,
            'table':Table.objects.all()
        }
        return render(request, 'owner/table.html', context)
    else:
        return redirect('/login/')
    
def menu_qrcode(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        context={
            'o':o
        }
        return render(request, 'owner/menu_qrcode.html', context)
    else:
        return redirect('/login/')
    
def category(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if 'add_category'in request.POST:
            name = request.POST.get('name')
            Category(
                name=name
            ).save()
            return redirect('category')
        if 'edit_category'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            c = Category.objects.filter(id=id).first()
            c.name = name
            c.save()
            return redirect('category')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Category.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('category')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Category.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('category')
        context={
            'o':o,
            'category':Category.objects.all()
        }
        return render(request, 'owner/category.html', context)
    else:
        return redirect('/login/')
    
def item(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if 'add_item'in request.POST:
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            price = request.POST.get('price')
            Item(
                name=name,
                category_id=category_id,
                price=price
            ).save()
            return redirect('item')
        if 'edit_item'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            price = request.POST.get('price')
            c = Item.objects.filter(id=id).first()
            c.name = name
            c.price = price
            c.category_id = category_id
            c.save()
            return redirect('item')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('item')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('item')
        context={
            'o':o,
            'category':Category.objects.filter(status = 1),
            'item':Item.objects.all()
        }
        return render(request, 'owner/item.html', context)
    else:
        return redirect('/login/')
    
def waiter(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if 'add_waiter'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            Waiter(
                name=name,
                mobile = mobile,
                pin = pin,
            ).save()
            return redirect('waiter')
        if 'edit_waiter'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            w = Waiter.objects.filter(id=id).first()
            w.name = name
            w.mobile = mobile
            w.pin = pin
            w.save()
            return redirect('waiter')
        if 'active'in request.POST:
            id = request.POST.get('id')
            w = Waiter.objects.filter(id=id).first()
            w.status = 0
            w.save()
            return redirect('waiter')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            w = Waiter.objects.filter(id=id).first()
            w.status = 1
            w.save()

        context={
            'o':o,
            'waiter':Waiter.objects.all(),        }
        return render(request, 'owner/waiter.html', context)
    else:
        return redirect('/login/')
    
def chef(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if 'add_chef'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            Chef(
                name=name,
                mobile = mobile,
                pin = pin,
            ).save()
            return redirect('chef')
        if 'edit_chef'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            w = Chef.objects.filter(id=id).first()
            w.name = name
            w.mobile = mobile 
            w.pin = pin
            w.save()
            return redirect('chef')
        if 'active'in request.POST:
            id = request.POST.get('id')
            w = Chef.objects.filter(id=id).first()
            w.status = 0
            w.save()
            return redirect('chef')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            w = Chef.objects.filter(id=id).first()
            w.status = 1
            w.save()

        context={
            'o':o,
            'chef':Chef.objects.all(),        }
        return render(request, 'owner/chef.html', context)
    else:
        return redirect('/login/')
    
def winner(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if 'add_url'in request.POST:
            id = request.POST.get('id')
            url = request.POST.get('url')
            lucky_draw = luckydrow_winner.objects.filter(id=id).first()
            lucky_draw.youtube_url = url
            lucky_draw.save()
            
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

def item_detail(request, id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            item = Item.objects.filter(id=id).first()
            if 'edit_item_name'in request.POST:
                name = request.POST.get('name')
                item.name = name
                item.save()
                return redirect(f'/owner/item_detail/{id}')
            if 'edit_price_name'in request.POST:
                price = request.POST.get('price')
                item.price = price
                item.save()
                return redirect(f'/owner/item_detail/{id}')
            if 'select_item_category'in request.POST:
                category_id = request.POST.get('id')
                ic = Select_item_category.objects.filter(item_id=id, category_id=category_id).first()
                if ic:
                    if ic.status == 0:
                        ic.status = 1
                        ic.save()
                else:
                    Select_item_category(
                        item_id=item.id,
                        category_id=category_id
                    ).save()
                return redirect(f'/owner/item_detail/{id}')
            if 'unselect_category'in request.POST:
                c_id = request.POST.get('id')
                ic = Select_item_category.objects.filter(item_id=id, category_id=c_id).first()
                ic.status = 0
                ic.save()
                return redirect(f'/owner/item_detail/{id}')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect(f'/owner/item_detail/{id}')
        if 'gst_active'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.gst_status = 0
            c.save()
            return redirect(f'/owner/item_detail/{id}')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect(f'/owner/item_detail/{id}')
        if 'gst_deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.gst_status = 1
            c.save()
            return redirect(f'/owner/item_detail/{id}')
        context={
            'o':o,
            'item':item,
            'category':Category.objects.filter(status=1),
            'Select_item_category':Select_item_category.objects.filter(item_id=item.id, status=1)
        }
        return render(request, 'owner/item_detail.html', context)
    else:
        return redirect('/login/')
    
    
@csrf_exempt
def view_order(request,table_id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            amount = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))
            amount = amount['total_amount__sum']
            if amount == None:
                amount = 0
            if 'Delete'in request.POST:
                cart_id = request.POST.get('cart_id')
                Hotel_cart.objects.filter(id=cart_id).delete()
                return redirect(f'/owner/view_order/{table_id}')
            if 'complete_order'in request.POST:
                order_filter = (int(Hotel_order_Master.objects.all().count()) + 1)
                t =Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
                if t != None:
                    ta = Hotel_cart.objects.filter(table_id=table_id, item__gst_status=0).aggregate(Sum('total_amount'))['total_amount__sum']
                    if ta != None:
                        t -= ta
                    
                gst = (t / 100) * 5
                s_gst = (gst / 2)
                c_gst = (gst / 2)
                total_price = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
                total_amount = math.floor(int(total_price) + int(gst))
                Hotel_order_Master(
                    table_id=table_id,
                    total_price=total_price,
                    order_filter=order_filter,
                    s_gst=s_gst,
                    c_gst=c_gst,
                    cash_amount=total_amount
                ).save()
                for i in Item.objects.filter(status=1):
                    if Hotel_cart.objects.filter(table_id=table_id, item_id=i.id):
                        Hotel_order_Detail(
                           item_id=i.id,
                           qty=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('qty'))['qty__sum'],
                           price=i.price,
                           total_price=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('total_amount'))['total_amount__sum'],
                           order_filter=order_filter
                        ).save()
                Hotel_cart.objects.filter(table_id=table_id).delete()
                return redirect(f'/owner/complate_view_order/{order_filter}')
        context={
            'o':o,
            'cart':Hotel_cart.objects.filter(table_id=table_id),
            'item':Item.objects.filter(status=1),
            'table_id':table_id,
            'amount':amount,
            'table':Table.objects.get(id=table_id),
            'category':Category.objects.filter(status=1)
            
        }
        return render(request, 'owner/view_order.html', context)
    else:
        return redirect('/login/')
                           
def complate_order(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            pass
        context={
            'o':o,
            'order_master':Hotel_order_Master.objects.all()
        }
        return render(request, 'owner/complate_order.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def complate_view_order(request,order_filter):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            bill_status = 0
            order_master = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
            if Bill.objects.filter(order_master__order_filter=order_filter).exists():
                bill_status = 1
            if 'Add_person_count'in request.POST:
                person_count = request.POST.get('person_count')
                Bill(
                    added_by_id = o.id,
                    order_master_id = order_master.id,
                    person_count=person_count,
                    scan_url=generate_url(),
                    ).save()
                return redirect(f'/owner/complate_view_order/{order_filter}')
            total_amount = math.floor(int(order_master.total_price) + order_master.s_gst + order_master.c_gst - int(order_master.discount_amount))
            if 'add_phone_pe_amount'in request.POST:
                phone_pe_amount = request.POST.get('phonepe_amount')
                order_master.phone_pe_amount = phone_pe_amount
                order_master.cash_amount -= float(phone_pe_amount)
                order_master.save()
                order_master = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
                return redirect(f'/owner/complate_view_order/{order_filter}')
            if 'edit_phone_pe_amount'in request.POST:
                phone_pe_amount = request.POST.get('phonepe_amount')
                old_amount = order_master.phone_pe_amount
                if old_amount > float(phone_pe_amount):
                    order_master.cash_amount +=  float(old_amount) - float(phone_pe_amount)
                else:
                    order_master.cash_amount -= float(phone_pe_amount) - float(old_amount) 
                order_master.phone_pe_amount = phone_pe_amount
                order_master.save()
                order_master = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
                order_master.save()
                return redirect(f'/owner/complate_view_order/{order_filter}')
            if 'add_pos_machine_amount'in request.POST:
                pos_machine_amount = request.POST.get('pos_machine_amount')
                order_master.pos_machine_amount = pos_machine_amount
                order_master.cash_amount -= float(pos_machine_amount)
                order_master.save()
                return redirect(f'/owner/complate_view_order/{order_filter}')
            if 'edit_pos_machine_amount'in request.POST:
                pos_machine_amount = request.POST.get('pos_machine_amount')
                old_amount = order_master.pos_machine_amount
                if old_amount > float(pos_machine_amount):
                    order_master.cash_amount +=  float(old_amount) - float(pos_machine_amount)
                else:
                    order_master.cash_amount -= float(pos_machine_amount) - float(old_amount) 
                order_master.pos_machine_amount = pos_machine_amount
                order_master.save()
                order_master = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
                order_master.save()
                return redirect(f'/owner/complate_view_order/{order_filter}')
            without_gst_amount = Hotel_order_Detail.objects.filter(order_filter=order_filter, item__gst_status=0).aggregate(Sum('total_price'))['total_price__sum']
        context={
            'o':o,
            'order_master':order_master,
            'order_detail':Hotel_order_Detail.objects.filter(order_filter=order_filter),
            'bill_status':bill_status,
            'total_amount':total_amount,
            'without_gst_amount':without_gst_amount
        }
        return render(request, 'owner/complate_view_order.html', context)
    else:
        return redirect('/login/')
    
