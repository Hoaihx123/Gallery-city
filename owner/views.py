from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist, Gallery
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
# Create your views here.

@user_passes_test(lambda u: u.is_owner == True)
def index(request):
    return render(request, 'owner/index.html')

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
            return redirect('/owner')
        except Owner.DoesNotExist:
            owner = Owner.objects.create(user=request.user, name=name, address=address, numphone=numphone)
            owner.save()
            return redirect('/owner/gallery')
    else:
        try:
            owner = Owner.objects.get(user=request.user)
            context = [owner.name, owner.address, owner.numphone]
            button = 'Save'
        except Owner.DoesNotExist:
            context = ['Name', 'Address', 'Number phone']
            button = 'Next'
        return render(request, 'owner/setting.html', {'context': context, 'button': button})

def gallery(request):
    try:
        owner = Owner.objects.get(user=request.user)
        if request.method == 'POST':
            name = request.POST['name']
            acreage = request.POST['acreage']
            address = request.POST['address']
            try:
                glr = Gallery.objects.get(owner=owner)
                glr.name = name
                glr.address = address
                glr.acreage = acreage
                glr.save()
                return redirect('/owner')
            except Gallery.DoesNotExist:
                glr = Gallery.objects.create(owner=owner, name=name, acreage=acreage, address=address)
                glr.save()
                return redirect('/owner')
        else:
            try:
                glr = Gallery.objects.get(owner=owner)
                context = [glr.name, glr.acreage, glr.address]
            except Gallery.DoesNotExist:
                context = ['Name', 'Acreage', 'Address']
            return render(request, 'owner/gallery.html', {'context': context})
    except Owner.DoesNotExist:
        if request.user.is_owner:
            return redirect('/owner/setting')
        else:
            return redirect('/')

