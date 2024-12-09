from django.shortcuts import render
from django.http import *
from customer.models import *
from owner.models import *
from django.template.loader import *
# Create your views here.
def participant_list(request):
    if request.method == 'GET':
        c = []
        p = participant.objects.filter(status=1)
        for p in p:
            c.append({'name':p.customer.name,'id':p.id})
        cr = list(c)
    return JsonResponse({'t': cr})

def save_winner(request):
    if request.method == 'GET':
        pass
    return JsonResponse({'t': 'cr'})

