from django.shortcuts import render
from django.http import *
from customer.models import *
from owner.models import *
from tea.models import *
from django.template.loader import *
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def chang_teble_status(request):
    if request.method == 'GET':
        id = request.GET['id']
        t = Table.objects.filter(id=id).first()
        if t.status == 1:
            t.status = 0
            t.save()
        else:
            t.status = 1
            t.save()
    t = render_to_string('ajax/chang_teble_status.html', {'t':t})
    return JsonResponse({'t':t})
def chang_teble_name(request):
    if request.method == 'GET':
        id = request.GET['id']
        name = request.GET['name']
        t = Table.objects.filter(id=id).first()
        t.table_number = name
        t.save()
        t = Table.objects.filter(id=id).first()
    t = render_to_string('ajax/chang_teble_status.html', {'t':t})
    return JsonResponse({'t':t})

def select_item_category(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        item_id = request.GET['item_id']
        category_item = Select_item_category.objects.filter(category_id=c_id,item_id=item_id).first()
        c = Category.objects.filter(id=c_id).first()
        if category_item:
            if category_item.status==0:
                category_item.status = 1
                category_item.save()
            else:
                category_item.status = 0
                category_item.save()
        else:
            Select_item_category(
                category_id=c_id,
                item_id=item_id,
            ).save()
    context = {
        'c':c
    }
    t = render_to_string('ajax/select_item_category.html', context)
    return JsonResponse({'t':t})


def search_tea_item_by_category(request):
    if request.method == 'GET':
        c_id = request.GET['c_id']
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        item_id = [] 
        for i in Select_category_item.objects.filter(category_id=c_id):
            item_id.append(i.item_id)
        context={
            'e': e,
            'item':Tea_item.objects.filter(id__in=item_id),
        }
        t = render_to_string('ajax/search_tea_item.html', context) 
    return JsonResponse({'t': t})

def participant_list(request):
    if request.method == 'GET':
        c = []
        p = participant.objects.filter(status=1)
        for p in p:
            c.append({'name':p.customer.name,'id':p.id})
        cr = list(c)
    return JsonResponse({'t': cr})

def search_tea_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        mobile = request.session['tea_mobile']
        e = Tea_employee.objects.filter(mobile=mobile, status=1).first()
        context={
                'item':Tea_item.objects.filter(name__icontains=words)[:3],
                'e':e
        }
        t = render_to_string('ajax/search_tea_item.html', context) 
    return JsonResponse({'t': t})

def search_hotel_item(request):
    if request.method == 'GET':
        words = request.GET['words']
        context={
                'item':Item.objects.filter(english_name__icontains=words)[:10],
        }
        t = render_to_string('ajax/filter_items_by_category.html', context) 
    return JsonResponse({'t': t})
import math
def select_discount_percent(request):
    if request.method == 'GET':
        order_filter = request.GET['order_filter']
        without_gst_amount = request.GET['without_gst_amount']
        percent = request.GET['percent']
        
        discount_amount = (int(math.floor(float(without_gst_amount))) / 100) * int(percent)
        print(discount_amount)
        
        order_master = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
        order_master.discount_amount = discount_amount
        order_master.discount_percent = percent
        
        total_amount = math.floor(int(order_master.total_price) - int(order_master.discount_amount))
        
        order_master.cash_amount = int(total_amount)
        order_master.phone_pe_amount = 0
        order_master.pos_machine_amount = 0
        
            
        order_master.save()

    return JsonResponse({'t': ''})

def add_item_to_cart(request):
    if request.method == 'GET':
        employee_id = request.GET['employee_id']
        item_id = request.GET['item_id']
        shope_id = request.GET['shope_id']
        price = request.GET['price']
        qty = request.GET['qty']
        total_amount = request.GET['total_amount']
        c = Cart.objects.filter(employee_id=employee_id, item_id=item_id).first()
        if c:
            c.qty = qty
            c.price = price
            c.total_amount = total_amount
            c.save()
        else:
            Cart(
                employee_id=employee_id,
                tea_shope_id=shope_id,
                item_id = item_id,
                price=price,
                qty=qty,
                total_amount=total_amount
            ).save()
        amount = Cart.objects.filter(employee_id=employee_id).aggregate(Sum('total_amount'))
        amount = amount['total_amount__sum']
        context={
                'cart':Cart.objects.filter(employee_id=employee_id),
        }
        t = render_to_string('ajax/item_to_cart.html', context) 
    return JsonResponse({'t': t,'amount':amount})

def add_item_to_cart_edit(request):
    if request.method == 'GET':
        item_id = request.GET['item_id']
        price = request.GET['price']
        qty = request.GET['qty']
        total_amount = request.GET['total_amount']
        order_filter = request.GET['order_filter']
        it = Item.objects.filter(id=item_id).first()
        Hotel_order_Detail(
            item_id=item_id,
            item_name=it.marathi_name,
            qty=qty,
            price=price,
            total_price=total_amount,
            order_filter=order_filter
        ).save()
        om = Hotel_order_Master.objects.filter(order_filter=order_filter).first()
        od = Hotel_order_Detail.objects.filter(order_filter=order_filter, item_id=item_id).first()
        om.total_price += od.total_price
        om.cash_amount += od.total_price
        om.phone_pe_amount = 0
        om.pos_machine_amount = 0
        om.discount_percent = 0
        om.discount_amount = 0
        om.save()
        
        
        
    return JsonResponse({'t': 't','amount':'amount'})

def cut_item_to_cart(request):
    if request.method == 'GET':
        employee_id = request.GET['employee_id']
        item_id = request.GET['item_id']
        price = request.GET['price']
        qty = request.GET['qty']
        total_amount = request.GET['total_amount']
        c = Cart.objects.filter(employee_id=employee_id, item_id=item_id).first()
        if int(qty) == 0:
            Cart.objects.filter(employee_id=employee_id, item_id=item_id).delete()
        else:
            c.qty = qty
            c.price = price
            c.total_amount = total_amount
            c.save()
        amount = Cart.objects.filter(employee_id=employee_id).aggregate(Sum('total_amount'))
        amount = amount['total_amount__sum']
        context={
                'cart':Cart.objects.filter(employee_id=employee_id),
        }
        t = render_to_string('ajax/item_to_cart.html', context) 
    return JsonResponse({'t': t,'amount':amount})

def add_item_to_hotel_cart(request):
    if request.method == 'GET':
        table_id = request.GET['table_id']
        item_id = request.GET['item_id']
        price = request.GET['price']
        qty = request.GET['qty']
        note = request.GET['note']
        if note == '':
            note = ' '
        total_amount = request.GET['total_amount']
        Hotel_cart(
            table_id=table_id,
            item_id = item_id,
            price=price,
            qty=qty,
            note=note,
            total_amount=total_amount
        ).save()
        amount = Hotel_cart.objects.filter(table_id=table_id).aggregate(Sum('total_amount'))
        amount = amount['total_amount__sum']
        context={
                'cart':Hotel_cart.objects.filter(table_id=table_id),
        }
        t = render_to_string('ajax/item_to_cart.html', context) 
    return JsonResponse({'t': t,'amount':amount})


def save_winner(request):
    if request.method == 'GET':
        winner_id = request.GET['winner_id']
        parti = participant.objects.filter(id=winner_id).first()
        p = participant.objects.filter(status=1)
        luckydrow_winner(            
                winner_participant_id=parti.id,
                total_participant=p.count()
        ).save()
        luckydrow = luckydrow_winner.objects.filter().last()
        for p in p:
            p = participant.objects.filter(id=p.id).first()
            p.lucky_drow = luckydrow.id
            p.status = 0
            p.save()
        bill = Bill.objects.filter(drow_status = 0)
        for bill in bill:
            bill = bill = Bill.objects.filter(id = bill.id).first()
            bill.drow_status = 1
            bill.status = 0
            bill.save()
    return JsonResponse({'t': 'cr'})


def filter_items_by_category(request):
    if request.method == 'GET':
        category_id = request.GET['category_id']
        
        item_id = []
        
        for i in Select_item_category.objects.filter(category_id=category_id, status = 1):
            item_id.append(i.item_id)
        
        items = Item.objects.filter(id__in=item_id, status=1)
        
        context = {
            'item': items,
        }
        t = render_to_string('ajax/filter_items_by_category.html', context)
    return JsonResponse({'t': t})


def select_category_item(request):
    if request.method == 'GET':
        category_id = request.GET['category_id']
        item_id = request.GET['item_id']
        s = Select_category_item.objects.filter(item_id=item_id,category_id=category_id).first()
        if s:
            if s.status == 1:
                status = 0
                s.status = 0
                s.save()
            else:
                status = 1
                s.status = 1
                s.save()
        else:
            status = 1
            Select_category_item(
                item_id=item_id,
                category_id=category_id
            ).save()
        return JsonResponse({'status': status})