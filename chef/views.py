from django.shortcuts import redirect, render
from .models import *
# Create your views here.
def chef_home(request):
    if request.session.has_key('chef_mobile'):
        mobile = request.session['chef_mobile']
        c = Chef.objects.filter(mobile=mobile, status=1).first()        
        context={
            'c':c
        }
        return render(request, 'chef/chef_home.html', context)
    else:
        return redirect('/login/')
    