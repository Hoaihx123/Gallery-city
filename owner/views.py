from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
# Create your views here.

@user_passes_test(lambda u: u.is_owner == True)
def setting(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        numphone = request.POST['numphone']
        try:
            owner = Owner.objects.get(user=request.user)
            owner.name = name
            owner.address = address
            owner.numphone = numphone
            owner.save()
            return redirect('/')
        except Owner.DoesNotExist:
            owner = Owner.objects.create(user=request.user, name=name, address=address, numphone=numphone)
            owner.save()
            return redirect('/')
    else:
        try:
            owner = Owner.objects.get(user=request.user)
            context = [owner.name, owner.address, owner.numphone]
            button = 'Save'
        except Owner.DoesNotExist:
            context = ['Name', 'Address', 'Number phone']
            button = 'Next'
        return render(request, 'owner/setting.html', {'context': context, 'button': button})