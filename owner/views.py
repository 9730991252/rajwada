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
from datetime import datetime, date, time
from django.core.paginator import Paginator
from django.contrib import messages 

# Create your views here.
def edit_bill(request,id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        om = Hotel_order_Master.objects.filter(id=id).first()
        ord = Hotel_order_Detail.objects.filter(order_filter=om.order_filter)
        amount = ord.aggregate(Sum('total_price'))['total_price__sum']
        if 'Delete'in request.POST:
            od_id = request.POST.get('cart_id')
            od = Hotel_order_Detail.objects.filter(id=od_id).first()
            om.total_price -= od.total_price
            om.cash_amount -= od.total_price
            om.phone_pe_amount = 0
            om.pos_machine_amount = 0
            om.save()
            od.delete()
            return redirect(f'/owner/edit_bill/{id}')
        context={
            'o':o,
            'om':Hotel_order_Master.objects.filter(id=id).first(),
            'ord':ord,
            'amount':amount,
            'category':Category.objects.filter(status=1),
            'item':Item.objects.filter(status=1),

        }
        return render(request, 'owner/edit_bill.html', context)
    else:
        return redirect('/login/')
    
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
    
def tea_shope(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()       
        if 'add_shope'in request.POST:
            hotel_name = request.POST.get('hotel_name') 
            hotel_address = request.POST.get('hotel_address') 
            h_mobile = request.POST.get('mobile') 
            branch_number = request.POST.get('branch_number')
            if Tea_shope.objects.filter(contact_number=h_mobile).exists():
                pass
            else:
                Tea_shope(
                    hotel_name=hotel_name,
                    hotel_address=hotel_address,
                    contact_number=h_mobile,
                    branch_number=branch_number
                ).save()
            return redirect('tea_shope')
        if 'edit_shope'in request.POST:
            id = request.POST.get('id')
            hotel_name = request.POST.get('hotel_name')
            hotel_address = request.POST.get('hotel_address')
            h_mobile = request.POST.get('mobile')
            branch_number = request.POST.get('branch_number')
            t = Tea_shope.objects.filter(id=id).first()
            t.hotel_name = hotel_name
            t.hotel_address = hotel_address
            t.contact_number = h_mobile
            t.branch_number = branch_number
            t.save()
            return redirect('tea_shope')
        context={
            'o':o,
            'tea_shope':Tea_shope.objects.all(),
        }
        return render(request, 'owner/tea_shope.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def report(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        item = []
        from_date = ''
        to_date = ''
        total_amount = 0
        total_cash = 0
        total_phone_pe = 0
        total_pos_machine = 0
        discount = 0
        if 'search_report' in request.POST:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            total_amount = 0
            for i in Item.objects.filter():
                qty = Hotel_order_Detail.objects.filter(item_id=i.id,date__range=[from_date, to_date] ).aggregate(Sum('qty'))['qty__sum']
                total_price = Hotel_order_Detail.objects.filter(item_id=i.id, date__range=[from_date, to_date]).aggregate(Sum('total_price'))['total_price__sum']
                
                if total_price == None:
                    total_price = 0
                total_amount += total_price
                if qty != None:
                    item.append({'name':i.marathi_name, 'qty':qty, 'total_price':total_price})  
                          
            total_cash = Hotel_order_Master.objects.filter(date__range=[from_date, to_date]).aggregate(Sum('cash_amount'))['cash_amount__sum']
            total_phone_pe = Hotel_order_Master.objects.filter(date__range=[from_date, to_date]).aggregate(Sum('phone_pe_amount'))['phone_pe_amount__sum']
            total_pos_machine = Hotel_order_Master.objects.filter(date__range=[from_date, to_date]).aggregate(Sum('pos_machine_amount'))['pos_machine_amount__sum']
            discount = Hotel_order_Master.objects.filter(date__range=[from_date, to_date]).aggregate(Sum('discount_amount'))['discount_amount__sum']

        context={
            'item':item,
            'from_date':from_date,
            'to_date':to_date,
            'total_amount':total_amount,
            'total_cash':total_cash,                
            'total_phone_pe':total_phone_pe,                
            'total_pos_machine':total_pos_machine,
            'discount':discount,
        }
        return render(request, 'owner/report.html', context)
    
    else:
        return redirect('login')
    
def tea_employee(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        if 'add_tea_employee'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            branch = request.POST.get('branch')
            Tea_employee(
                name=name,
                mobile = mobile,
                pin = pin,
                tea_shope_id = branch
            ).save()
            return redirect('tea_employee')
        if 'edit_tea_employee'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            branch = request.POST.get('branch')
            w = Tea_employee.objects.filter(id=id).first()
            w.name = name
            w.mobile = mobile
            w.pin = pin
            w.tea_shope_id = branch
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
            'tea_employee':Tea_employee.objects.all(),
            'tea_shope':Tea_shope.objects.filter(status=1),
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
        if 'chang_table'in request.POST:
            old = request.POST.get('old_table')
            new = request.POST.get('new_table')
            h = Hotel_cart.objects.filter(table_id=old).first()
            h.table_id = new
            h.save()
            return redirect('running_table')
        context={
            'o':o,
            'table':table,
            'runing_table':runing_table,
            'unpaid_bills':Hotel_order_Master.objects.filter(paid_status=0).order_by('-id')[0:10]
        }
        return render(request, 'owner/running_table.html', context)
    else:
        return redirect('/login/')
    
@csrf_exempt
def table(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()
        if 'add_table'in request.POST:
            table_number = request.POST.get('name')
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
            'table':Table.objects.all(),
            'next_table_count':Table.objects.all().count()+1
            
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
            return redirect('/owner/category/')
        if 'edit_category'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            c = Category.objects.filter(id=id).first()
            c.name = name
            c.save()
            return redirect('/owner/category/')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Category.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('/owner/category/')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Category.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('/owner/category/')
        if 'save_order_by'in request.POST:
            c_id = request.POST.get('id')
            order_by = request.POST.get('order_by')
            c = Category.objects.filter(id=c_id).first()
            c.order_by = order_by
            c.save()
            return redirect('/owner/category/')
        context={
            'o':o,
            'category':Category.objects.all().order_by('-order_by')
        }
        return render(request, 'owner/category.html', context)
    else:
        return redirect('/login/')
    
def item(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()      
        if 'add_item'in request.POST:  
            marathi_name = request.POST.get('marathi_name')
            english_name = request.POST.get('english_name')
            price = request.POST.get('price')
            Item(
                marathi_name=marathi_name,
                english_name=english_name,
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

@csrf_exempt
def item_detail(request, id):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            item = Item.objects.filter(id=id).first()
            if 'discount_active' in request.POST:
                item.discount_status = 0
                item.save()
                print('hi')
                return redirect('item_detail', id=id)
            if 'discount_deactive'in request.POST:
                item.discount_status = 1
                item.save()
                return redirect('item_detail', id=id)
            if 'edit_item_marathi_name' in request.POST:
                name = request.POST.get('marathi_name')
                item.marathi_name = name
                item.save()
                return redirect('item_detail', id=id)
            if 'edit_item_english_name' in request.POST:
                name = request.POST.get('english_name')
                item.english_name = name
                item.save()
                return redirect('item_detail', id=id)
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
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 1
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
                messages.warning(request,f"Removed SuccessFully.")
                return redirect(f'/owner/view_order/{table_id}')
            if 'complete_order'in request.POST:
                order_filter = (int(Hotel_order_Master.objects.all().count()) + 1)
                
                comolete_order(order_filter, table_id)
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
    
def comolete_order(order_filter, table_id):
    t =Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
    if t != None:
        ta = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
        if ta != None:
            t -= ta
        
    total_price = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))['total_amount__sum']
    total_amount = math.floor(int(total_price))
    Hotel_order_Master(
        table_id=table_id,
        total_price=total_price,
        order_filter=order_filter,
        cash_amount=total_amount,        
    ).save()
    for i in Item.objects.filter(status=1):
        if Hotel_cart.objects.filter(table_id=table_id, item_id=i.id):
            Hotel_order_Detail(
               item_id=i.id,
               qty=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('qty'))['qty__sum'],
               price=i.price,
               total_price=Hotel_cart.objects.filter(table_id=table_id, item_id=i.id).aggregate(Sum('total_amount'))['total_amount__sum'],
               order_filter=order_filter,
                item_name=i.marathi_name,
            ).save()
    Hotel_cart.objects.filter(table_id=table_id).delete()
                           
def complate_order(request):
    if request.session.has_key('owner_mobile'):
        mobile = request.session['owner_mobile']
        o = Owner.objects.filter(mobile=mobile, status=1).first()        
        if o:
            if 'cancel_bill'in request.POST:
                order_filter = request.POST.get('order_filter')
                om = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
                om.status = 0
                om.save()
                return redirect('complate_order')
            order_master = []
            for b in Hotel_order_Master.objects.filter().order_by('-id'):
                cancel_btn_show_status = 0
                order_details = Hotel_order_Detail.objects.filter(order_filter=b.order_filter).first()
                if order_details:
                    if order_details.date == date.today():
                        cancel_btn_show_status = 1
                order_master.append({
                    'id': b.id,
                    'order_filter': b.order_filter,
                    'total_price': b.total_price,
                    'ordered_date': b.ordered_date,
                    'status':b.status,
                    'cancel_btn_show_status':cancel_btn_show_status
                })
            paginator = Paginator(order_master, per_page=100)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        context={
            'o':o,
            'order_master':page_obj
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
            total_amount = math.floor(int(order_master.total_price) - int(order_master.discount_amount))
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
            discount_amount = Hotel_order_Detail.objects.filter(order_filter=order_filter, item__discount_status=1).aggregate(Sum('total_price'))['total_price__sum']
            if 'chang_paid_status'in request.POST:
                order_master.paid_status = 1
                order_master.save()
                return redirect(f'/owner/complate_view_order/{order_filter}')
                
        context={
            'o':o,
            'order_master':order_master,
            'order_detail':Hotel_order_Detail.objects.filter(order_filter=order_filter),
            'bill_status':bill_status,
            'total_amount':total_amount,
            'bill':Bill.objects.filter(order_master__order_filter=order_filter).first(),
            'discount_amount':discount_amount
        }
        return render(request, 'owner/complate_view_order.html', context)
    else:
        return redirect('/login/')
    
