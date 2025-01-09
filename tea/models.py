from django.db import models

# Create your models here.
class Tea_employee(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.IntegerField(unique=True)
    pin = models.IntegerField()
    status=models.IntegerField(default=1)

class Tea_item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    status = models.IntegerField(default=1) 
    
class Cart(models.Model):
    employee = models.ForeignKey(Tea_employee,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Tea_item,on_delete=models.PROTECT,null=True)
    price = models.FloatField()
    total_amount = models.FloatField(default=0)
    qty = models.IntegerField()

class Tea_profile(models.Model):
    hotel_name = models.CharField(max_length=100,default='')
    contact_number=models.IntegerField(unique=True)
    hotel_address = models.CharField(max_length=100,default='')
    status=models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True, null=True)


class OrderMaster(models.Model):
    employee = models.ForeignKey(Tea_employee,on_delete=models.PROTECT,null=True)
    total_price=models.FloatField(default=0,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    order_filter=models.IntegerField(default=True)
    
    
class OrderDetail(models.Model):
    employee = models.ForeignKey(Tea_employee,on_delete=models.PROTECT,null=True)
    item=models.ForeignKey(Tea_item,on_delete=models.PROTECT,null=True)
    qty = models.IntegerField(default=1)
    price=models.FloatField(default=0,null=True)
    total_price=models.FloatField(default=0,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)
    date=models.DateField(auto_now_add=True,null=True)
    order_filter=models.IntegerField(default=True)
    
    
class Tea_category(models.Model):
    name = models.CharField(max_length=100)
    order_by = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    
    
class Select_category_item(models.Model):
    category = models.ForeignKey(Tea_category,on_delete=models.PROTECT,null=True)
    item = models.ForeignKey(Tea_item,on_delete=models.PROTECT,null=True)
    status = models.IntegerField(default=1)