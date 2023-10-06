from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist, Work, Notification, Work_Exhibit, Place, Exhibit
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.db import connection
# Create your views here.


@user_passes_test(lambda u: u.is_artist == True)
def manage(request):
    try:
        artist = Artist.objects.get(user=request.user)
        cur = connection.cursor()
        cur.execute(f"Select count(*) from core_notification WHERE user_id={artist.user_id} and is_seen=False")
        num = cur.fetchone()
        cur.execute(f"select e.name, start_time, end_time, e.type, g.name, g.address, e.id, e.gallery_id from "
                    f"core_place p join core_exhibit e on p.exhibit_id=e.id and artist_id={artist.user_id} and end_time>to_char(now(), 'YYYY-MM-DD')" 
									"join core_gallery g on g.owner_id=gallery_id order by start_time ")
        datas = cur.fetchall()
        context = {'artist': artist, 'num': num, 'datas': datas}
        return render(request, 'artist/manage.html', context)
    except Artist.DoesNotExist:
        return redirect('../artist/setting')

@user_passes_test(lambda u: u.is_artist == True)
def setting(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        birthday = str(request.POST['birthday'])
        bio = request.POST['bio']
        education = request.POST['education']
        try:
            artist = Artist.objects.get(user=request.user)
            artist.name = name
            if request.FILES.get('img') != None:
                img = request.FILES.get('img')
                artist.img = img
            artist.address = address
            artist.birthday = birthday
            artist.bio = bio
            artist.education = education
            artist.save()
        except Artist.DoesNotExist:
            if request.FILES.get('img')!=None:
                img = request.FILES.get('img')
                artist = Artist.objects.create(user=request.user, name=name, address=address, birthday=birthday, bio=bio, education=education, img=img)
            else:
                artist = Artist.objects.create(user=request.user, name=name, address=address, birthday=birthday, bio=bio, education=education)
            artist.save()
        return redirect('../artist')
    else:
        try:
            artist = Artist.objects.get(user=request.user)
            context = [artist.name, artist.address, artist.birthday, artist.bio, artist.education]
        except Artist.DoesNotExist:
            context = ['Name', 'Address', 'Birthday', 'Biograph', 'Education']
        return render(request, 'artist/setting.html', {'context': context})

def add_work(request):
    try:
        artist = Artist.objects.get(user=request.user)
        if request.method == 'POST':
            name = request.POST['name']
            execution = request.POST['type']
            height = request.POST['height']
            width = request.POST['width']
            volume = request.POST['volume']
            img = request.FILES.get('img')
            if volume == '':
                new_work = Work.objects.create(artist=artist, name=name, execution=execution, height=height,
                                               width=width, img=img)
            else:
                new_work = Work.objects.create(artist=artist, name=name, execution=execution, height=height, width=width, volume=volume, img=img)
            new_work.save()
            return redirect('../artist/work_manage')
        else:
            cur = connection.cursor()
            cur.execute(f"Select count(*) from core_notification WHERE user_id={artist.user_id} and is_seen=False")
            num = cur.fetchone()
            context = {'artist': artist, 'num': num}
            return render(request, 'artist/add_work.html', context)
    except Artist.DoesNotExist:
        return redirect('../artist/setting')

@user_passes_test(lambda u: u.is_artist == True)
def work_manage(request):
    try:
        artist = Artist.objects.get(user=request.user)
        if request.method == 'POST':
            work_id = request.POST['work_id']
            cur = connection.cursor()
            cur.execute(f"DELETE FROM core_work WHERE id={work_id}")
            return redirect('/artist/work_manage')
        else:
            works = Work.objects.filter(artist=artist)
            works = reversed(works)
            cur = connection.cursor()
            cur.execute(f"Select count(*) from core_notification WHERE user_id={artist.user_id} and is_seen=False")
            num = cur.fetchone()
            context = {'artist': artist, 'works': works, 'num': num}
            return render(request, 'artist/work_manage.html', context)
    except Artist.DoesNotExist:
        return redirect('../artist/setting')

def register(request, exhibit_id):
    try:
        artist = Artist.objects.get(user=request.user)
        exhibit = Exhibit.objects.get(id=exhibit_id)
        if request.method == 'POST':
            works_id = request.POST.getlist('work')
            if len(works_id):
                for work_id in works_id:
                    if Work_Exhibit.objects.filter(exhibit_id=exhibit_id, work_id=work_id).exists()==False:
                        new_we = Work_Exhibit.objects.create(exhibit_id=exhibit_id, work_id=work_id)
                        new_we.save()
                if Place.objects.filter(artist=artist, exhibit_id=exhibit_id).exists()==False:
                    new_place = Place.objects.create(artist=artist, exhibit_id=exhibit_id)
                    content = 'Artist '+artist.name+' have agreed to participate in your event '+exhibit.name
                    new_ntf = Notification.objects.create(user_id=exhibit.gallery.owner_id, exhibit=exhibit, content=content)
                    new_ntf.save()
                    new_place.save()
            return redirect('../')

        else:
            works = Work.objects.filter(artist=artist)
            cur = connection.cursor()
            cur.execute(f"Select count(*) from core_notification WHERE user_id={artist.user_id} and is_seen=False")
            num = cur.fetchone()
            context = {'artist': artist, 'works': works, 'num': num}
            return render(request, 'artist/register.html', context)
    except:
        return redirect('../artist/setting')

@user_passes_test(lambda u: u.is_artist == True)
def info(request):
    try:
        artist = Artist.objects.get(user=request.user)
        notifications = Notification.objects.filter(user=request.user)
        notifications = reversed(notifications)
        cur = connection.cursor()
        cur.execute(f"Update core_notification set is_seen=True where user_id={artist.user_id}")
        context = {'artist': artist, 'notifications': notifications}
        return render(request, 'artist/info.html', context)
    except Artist.DoesNotExist:
        return redirect('../artist/setting')

def update_work(request, work_id):
    try:
        work = Work.objects.get(id=work_id)
        if work.artist.user_id == request.user.id:
            if request.method == 'POST':
                work.name = request.POST['name']
                work.execution = request.POST['type']
                work.height = request.POST['height']
                work.width = request.POST['width']
                if request.POST['volume'] != '':
                    work.volume = request.POST['volume']
                if request.FILES.get('img'):
                    work.img = request.FILES.get('img')
                work.save()
                return redirect('../work_manage')
            else:
                artist = Artist.objects.get(user=request.user)
                cur = connection.cursor()
                cur.execute(f"Select count(*) from core_notification WHERE user_id={artist.user_id} and is_seen=False")
                num = cur.fetchone()
                context = {'artist': artist, 'work': work, 'num': num}
                return render(request, 'artist/update_work.html', context)
        else:
            return redirect('/')
    except:
        return redirect('/')