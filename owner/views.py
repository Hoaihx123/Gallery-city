from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist, Gallery, Exhibit, Notification
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.db import connection
from django.http import JsonResponse
# Create your views here.


@user_passes_test(lambda u: u.is_owner == True)
def manage(request):
    try:
        owner = Owner.objects.get(user=request.user)
        try:
            if request.method == 'POST':
                id = request.POST['exhibit_id']
                cur = connection.cursor()
                cur.execute(f"DELETE FROM core_exhibit WHERE id={id}")
                return redirect('../owner')
            else:
                glr = Gallery.objects.get(owner=owner)
                exhibits = Exhibit.objects.filter(gallery=glr)
                exhibits = reversed(exhibits)
                cur = connection.cursor()
                cur.execute(f"Select count(*) from core_notification WHERE user_id={owner.user_id} and is_seen=False")
                num = cur.fetchone()
                context = {'glr': glr, 'exhibits': exhibits,
                           'owner_img': owner.img, 'num': num}
                return render(request, 'owner/manage.html', context)
        except Gallery.DoesNotExist:
            return redirect('../owner/gallery')
    except Owner.DoesNotExist:
        return redirect('../owner/setting')


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
                img = request.FILES.get('img')
                new_exhibit = Exhibit.objects.create(gallery=glr, name=name, start_time=start_time,
                                                     end_time=end_time, type=type, num_of_tickets=num_of_tickets, price=price, img=img)
                new_exhibit.save()

                return redirect('../owner')
            else:
                cur = connection.cursor()
                cur.execute(f"Select count(*) from core_notification WHERE user_id={owner.user_id} and is_seen=False")
                num = cur.fetchone()
                return render(request, 'owner/create_exhibit.html', {'glr': glr, 'owner_img': owner.img, 'num': num})
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
            img = request.FILES.get('img')
            owner = Owner.objects.create(
                user=request.user, name=name, address=address, numphone=numphone, img=img)
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
            description = request.POST['description']
            try:
                glr = Gallery.objects.get(owner=owner)
                glr.name = name
                glr.address = address
                glr.acreage = acreage
                glr.description = description
                if request.FILES.get('img') != None:
                    glr.img = request.FILES.get('img')
                glr.save()
                return redirect('/owner')
            except Gallery.DoesNotExist:
                img = request.FILES.get('img')
                glr = Gallery.objects.create(
                    owner=owner, name=name, acreage=acreage, address=address, img=img, description=description)
                glr.save()
                return redirect('/owner')
        else:
            try:
                glr = Gallery.objects.get(owner=owner)
                context = [glr.name, glr.acreage, glr.address, glr.description]
            except Gallery.DoesNotExist:
                context = ['Name', 'Acreage', 'Address', 'Description']
            return render(request, 'owner/gallery.html', {'context': context})
    except Owner.DoesNotExist:
        if request.user.is_owner:
            return redirect('/owner/setting')
        else:
            return redirect('/')

def add_artists(request, exhibit_id):
    try:
        owner = Owner.objects.get(user=request.user)
        try:
            if request.method == 'POST':
                content = request.POST['content']
                try:
                    id_artists = request.POST.getlist('artist')
                    exhibit = Exhibit.objects.get(id=exhibit_id)
                    for id_artist in id_artists:
                        new_nf = Notification.objects.create(user_id=id_artist, content=content, is_invitation=True, exhibit=exhibit)
                        new_nf.save()
                    return redirect('../')
                except:
                    return redirect('../')
            else:
                glr = Gallery.objects.get(owner=owner)
                exhibit = Exhibit.objects.get(id=exhibit_id)
                artists = Artist.objects.all()
                cur = connection.cursor()
                cur.execute(f"Select count(*) from core_notification WHERE user_id={owner.user_id} and is_seen=False")
                num = cur.fetchone()
                context = {'owner_img': owner.img, 'glr': glr, 'exhibit': exhibit, 'artists': artists, 'num': num}
                return render(request, 'owner/add_artists.html', context)
        except Gallery.DoesNotExist:
            return redirect('owner/gallery')
    except Owner.DoesNotExist:
        return redirect('owner/setting')

def info(request):
    try:
        owner = Owner.objects.get(user=request.user)
        try:
            glr = Gallery.objects.get(owner=owner)
            ntfs = Notification.objects.filter(user=request.user)
            ntfs = reversed(ntfs)
            cur = connection.cursor()
            cur.execute(f"Update core_notification set is_seen=True where user_id={owner.user_id}")
            context = {'owner_img': owner.img, 'ntfs': ntfs, 'glr': glr}
            return render(request, 'owner/info.html', context)
        except Gallery.DoesNotExist:
            return redirect('../owner/gallery')
    except Owner.DoesNotExist:
        return redirect('../owner/setting')

