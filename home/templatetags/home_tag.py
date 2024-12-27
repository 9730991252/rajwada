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
        
    

# @register.inclusion_tag('inclusion_tag/office/pendding_completed_farmer_bill.html')
# def pendding_completed_farmer_bill(farmer_id):
#     if farmer_id:
#         farmer_bill = Farmer_bill.objects.filter(farmer_id=farmer_id)
#         total_amount = farmer_bill.aggregate(Sum('total_amount'))
#         total_amount = total_amount['total_amount__sum']
#         print(total_amount)
        