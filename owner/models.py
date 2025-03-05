from django.db import models
from embed_video.fields import EmbedVideoField 

# Create your models here.
class Owner(models.Model):
    hotel_name = models.CharField(max_length=100,default='')
    owner_name=models.CharField(max_length=100)
    mobile=models.IntegerField(unique=True)
    pin = models.IntegerField()
    hotel_address = models.CharField(max_length=100,default='')
    status=models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    order_by = models.IntegerField(default=0,null=True)
    
class Item(models.Model):
    marathi_name = models.CharField(max_length=100, default='')
    english_name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    status = models.IntegerField(default=1)
    discount_status = models.IntegerField(default=0)

    
class Select_item_category(models.Model):
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    status = models.IntegerField(default=1)

class Table(models.Model):
    table_number = models.CharField(max_length=100)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)
    
    
class Hotel_cart(models.Model):
    table = models.ForeignKey(Table,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    price = models.FloatField()
    total_amount = models.FloatField(default=0)
    qty = models.IntegerField()
    note = models.CharField(null=True, max_length=100)
    cook_status = models.CharField(default='Pendding', max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
class Hotel_order_Master(models.Model):
    table=models.ForeignKey(Table,on_delete=models.PROTECT,default=True)
    total_price=models.FloatField(default=0,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    order_filter=models.IntegerField(default=True)
    date = models.DateField(auto_now=True,null=True)
    discount_percent = models.IntegerField(default=0)
    discount_amount = models.FloatField(default=0, null=True)
    cash_amount = models.FloatField(default=0, null=True)
    phone_pe_amount = models.FloatField(default=0, null=True)
    pos_machine_amount = models.FloatField(default=0, null=True) 
    paid_status = models.IntegerField(default=0)
    status = models.IntegerField(default=1)


    

class Hotel_order_Detail(models.Model):
    item=models.ForeignKey(Item,on_delete=models.PROTECT,null=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    date = models.DateField(auto_now_add=True,null=True)
    item_name = models.CharField(max_length=100, null=True)
    
class Bill(models.Model):
    added_by = models.ForeignKey(Owner,on_delete=models.PROTECT,null=True)
    order_master = models.ForeignKey(Hotel_order_Master,on_delete=models.PROTECT,null=True)
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
    youtube_url = EmbedVideoField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)