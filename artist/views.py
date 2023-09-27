from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from core.models import User, Owner, Artist
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

# Create your views here.

@user_passes_test(lambda u: u.is_artist == True)
def setting(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        # birthday = datetime.strptime(request.POST['birthday'], '%Y-%m-%d').time()
        birthday = str(request.POST['birthday'])
        bio = request.POST['bio']
        education = request.POST['education']
        try:
            artist = Artist.objects.get(user=request.user)
            artist.name = name
            artist.address = address
            artist.birthday = birthday
            artist.bio = bio
            artist.education = education
            artist.save()
        except Artist.DoesNotExist:
            artist = Artist.objects.create(user=request.user, name=name, address=address, birthday=birthday, bio=bio, education=education)
            artist.save()
        return redirect('/')
    else:
        try:
            artist = Artist.objects.get(user=request.user)
            context = [artist.name, artist.address, artist.birthday, artist.bio, artist.education]
        except Artist.DoesNotExist:
            context = ['Name', 'Address', 'Birthday', 'Biograph', 'Education']
        return render(request, 'artist/setting.html', {'context': context})
