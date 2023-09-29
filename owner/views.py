from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist, Gallery, Exhibit
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.db import connection
# Create your views here.

@user_passes_test(lambda u: u.is_owner == True)
def manage(request):
    try:
        owner = Owner.objects.get(user=request.user)
        try:
            if request.method == 'POST':
                id=request.POST['exhibit_id']
                cur = connection.cursor()
                cur.execute(f"DELETE FROM core_exhibit WHERE id={id}")
                return redirect('../owner')
            else:
                glr = Gallery.objects.get(owner=owner)
                exhibits = Exhibit.objects.filter(gallery=glr)
                context = {'glr': glr, 'exhibits': exhibits}
                return render(request, 'owner/manage.html', context)
        except Gallery.DoesNotExist:
            return redirect('owner/gallery')
    except Owner.DoesNotExist:
        return redirect('owner/setting')

@user_passes_test(lambda u: u.is_owner == True)
def create_exhibit(request):
    try:
        owner = Owner.objects.get(user=request.user)
        try:
            glr = Gallery.objects.get(owner=owner)
            if request.method == 'POST':
                name = request.POST['name']
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                type = request.POST['type']
                num_of_tickets = request.POST['num_of_tickets']
                price = request.POST['price']
                new_exhibit = Exhibit.objects.create(gallery=glr, name=name, start_time=start_time, end_time=end_time, type=type, num_of_tickets=num_of_tickets, price=price)
                new_exhibit.save()
                return redirect('../owner')
            else:
                return render(request, 'owner/create_exhibit.html')
        except Gallery.DoesNotExist:
            return redirect('owner/gallery')
    except Owner.DoesNotExist:
        return redirect('owner/setting')


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

