from django import template
from owner.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from tea.models import *
from waiter.models import * 
from chef.models import * 
from datetime import datetime, date, time

register = template.Library()

@register.simple_tag()
def customer_selected_item_count(category_id):
    return Select_item_category.objects.filter(category_id=category_id,status = 1).count()


@register.simple_tag()
def cart_item_detail(item_id, employee_id):
    cart = Cart.objects.filter(item_id=item_id,employee_id=employee_id).first()
    if cart:
        return {'qty':cart.qty, 'amount':cart.total_amount}
    else:
        return {'qty':0, 'amount':0}
    
@register.simple_tag()
def todayes_tea_total():
    t =  OrderMaster.objects.filter(ordered_date__icontains=date.today()).aggregate(Sum('total_price'))
    t =  t['total_price__sum']
    if t:
        return t
    else:
        return 0
        
@register.simple_tag()
def hotel_cart_item_detail(table_id, item_id):
    cart = Hotel_cart.objects.filter(item_id=item_id,table_id=table_id).first()
    if cart:
        return {'qty':cart.qty, 'amount':cart.total_amount}
    else:
        return {'qty':0, 'amount':0}
    
@register.simple_tag()
def get_percenteg_amount(percent, without_gst_amount):
    if without_gst_amount:
        return (int(math.floor(float(without_gst_amount))) / 100) * int(percent)    
    else:
        return 0
    
    
@register.simple_tag()
def category_selected_item(category_id):
    category = Category.objects.filter(id=category_id).first()
    item = []
    for i in Item.objects.filter():
        selected_status = 0
        if Select_item_category.objects.filter(item_id=i.id,category_id=category.id,status = 1):
            selected_status = 1 
        print(selected_status)
        item.append({'name':i.marathi_name, 'selected_status':selected_status ,'id':i.id})
    return item

# @register.inclusion_tag('inclusion_tag/office/pendding_completed_farmer_bill.html')
# def pendding_completed_farmer_bill(farmer_id):
#     if farmer_id:
#         farmer_bill = Farmer_bill.objects.filter(farmer_id=farmer_id)
#         total_amount = farmer_bill.aggregate(Sum('total_amount'))
#         total_amount = total_amount['total_amount__sum']
#         print(total_amount)
        
        
@register.inclusion_tag('inclusion_tag/owner/todays_sell.html')
def todays_sell():
    
    item = []
    total_amount = 0
    for i in Item.objects.filter():
        qty = Hotel_order_Detail.objects.filter(item_id=i.id,date__range=[date.today(), date.today()] ).aggregate(Sum('qty'))['qty__sum']
        total_price = Hotel_order_Detail.objects.filter(item_id=i.id, date__range=[date.today(), date.today()]).aggregate(Sum('total_price'))['total_price__sum']
        if total_price == None:
            total_price = 0
        total_amount += total_price
        if qty != None:
            item.append({'name':i.marathi_name, 'qty':qty, 'total_price':total_price})        
    ft_date = date(date.today().year, date.today().month, date.today().day)
    ft_time = time(00, 00, 00)
    from_date = datetime.combine(ft_date, ft_time)
    print(from_date)
    
    day = int(date.today().day) + 1
    
    t_date = date(date.today().year, date.today().month, day)
    t_time = time(00, 00, 00)
    to_date = datetime.combine(t_date, t_time)
    
    total_cash = Hotel_order_Master.objects.filter(ordered_date__range=[from_date, to_date]).aggregate(Sum('cash_amount'))['cash_amount__sum']
    total_phone_pe = Hotel_order_Master.objects.filter(ordered_date__range=[from_date, to_date]).aggregate(Sum('phone_pe_amount'))['phone_pe_amount__sum']
    total_pos_machine = Hotel_order_Master.objects.filter(ordered_date__range=[from_date, to_date]).aggregate(Sum('pos_machine_amount'))['pos_machine_amount__sum']
    discount = Hotel_order_Master.objects.filter(ordered_date__range=[from_date, to_date]).aggregate(Sum('discount_amount'))['discount_amount__sum']
    return{
        'item':item,
        'total_amount':total_amount,
        'total_cash':total_cash,
        'total_phone_pe':total_phone_pe,
        'total_pos_machine':total_pos_machine,
        'discount':discount,        
        }