from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import User, Owner, Artist, Gallery, Exhibit
# Create your views here.


@login_required(login_url='core:signin')
def index(request):

    galleries = Gallery.objects.all()
    exhibits = Exhibit.objects.raw("SELECT * from core_exhibit where start_time>to_char(now(), 'YYYY-MM-DD') order by start_time")
    context = {'galleries': galleries, 'exhibits': exhibits, 'username': request.user.username}
    return render(request, 'core/home.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_owner:
                return redirect('owner/')
            if user.is_artist:
                return redirect('artist/')
            else:
                return redirect('/')
        else:
            messages.info(request, "Username or password incorrect")
            return redirect('core:signin')
    else:
        return render(request, 'core/signin.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        type = request.POST['type']
        if password == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.info(request, "Email or user was used")
                return redirect('signup')
            else:
                if type == 'owner':
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.is_owner = True
                    user.save()
                    user_login = auth.authenticate(
                        username=username, password=password)
                    auth.login(request, user_login)
                    return redirect('owner/setting')
                if type == 'artist':
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.is_artist = True
                    user.save()
                    user_login = auth.authenticate(
                        username=username, password=password)
                    auth.login(request, user_login)
                    return redirect('artist/setting')
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    user_login = auth.authenticate(
                        username=username, password=password)
                    auth.login(request, user_login)
                    return redirect('/')
        else:
            messages.info(request, "Password no matching")
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')


@login_required(login_url='core:signin')
def logout(request):
    auth.logout(request)
    return redirect('/')
