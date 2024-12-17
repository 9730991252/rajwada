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

