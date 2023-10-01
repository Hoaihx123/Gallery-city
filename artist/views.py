from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist, Work
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.db import connection
# Create your views here.


@user_passes_test(lambda u: u.is_artist == True)
def manage(request):
    try:
        artist = Artist.objects.get(user=request.user)
        context = {'artist': artist}
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

@user_passes_test(lambda u: u.is_artist == True)
def add_work(request):
    try:
        artist = Artist.objects.get(user=request.user)
        if request.method == 'POST':
            name = request.POST['name']
            execution = request.POST['type']
            height = request.POST['height']
            width = request.POST['height']
            volume = request.POST['volume']
            img = request.FILES.get('img')
            new_work = Work.objects.create(artist=artist, name=name, execution=execution, height=height, width=width, volume=volume, img=img)
            new_work.save()
            return redirect('../artist/work_manage')
        else:
            context = {'artist': artist}
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
            return redirect('work_manage')
        else:
            works = Work.objects.filter(artist=artist)
            works = reversed(works)
            context = {'artist': artist, 'works': works}
            return render(request, 'artist/work_manage.html', context)
    except:
        return redirect('../artist/setting')
