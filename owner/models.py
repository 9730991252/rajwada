from django.db import models

# Create your models here.
class Owner(models.Model):
    hotel_name = models.CharField(max_length=100,default='')
    owner_name=models.CharField(max_length=100)
    mobile=models.IntegerField(unique=True)
    pin = models.IntegerField()
    hotel_address = models.CharField(max_length=100,default='')
    status=models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    
class Bill(models.Model):
    added_by = models.ForeignKey(Owner,on_delete=models.PROTECT,null=True)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    person_count = models.IntegerField()
    drow_status = models.IntegerField(default=0)
    scan_url = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class participant(models.Model):
    bill = models.ForeignKey(Bill,on_delete=models.PROTECT,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,null=True)
    lucky_drow = models.CharField(max_length=100, default=0)
    date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)
    
class luckydrow_winner(models.Model):
    winner_participant = models.ForeignKey(participant,on_delete=models.PROTECT,null=True)
    total_participant = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)
    