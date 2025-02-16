from django import template
from owner.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from tea.models import *
register = template.Library()
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
    
    

# @register.inclusion_tag('inclusion_tag/office/pendding_completed_farmer_bill.html')
# def pendding_completed_farmer_bill(farmer_id):
#     if farmer_id:
#         farmer_bill = Farmer_bill.objects.filter(farmer_id=farmer_id)
#         total_amount = farmer_bill.aggregate(Sum('total_amount'))
#         total_amount = total_amount['total_amount__sum']
#         print(total_amount)
        