from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import User, Owner, Artist, Gallery, Exhibit, Place, Work_Exhibit, Work
# Create your views here.


def test_layout(request):
    return render(request, "core/layout.html")


@login_required(login_url='core:signin')
def index(request):
    galleries = Gallery.objects.all()
    exhibits = Exhibit.objects.raw(
        "SELECT * from core_exhibit where start_time>to_char(now(), 'YYYY-MM-DD') order by start_time")
    context = {'galleries': galleries, 'exhibits': exhibits,
               'username': request.user.username}

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
                return redirect('core:signup')
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
            return redirect('core:signup')
    else:
        return render(request, 'core/signup.html')


@login_required(login_url='core:signin')
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='core:signin')
def exhibit_view(request, exhibit_id):
    exhibit = Exhibit.objects.get(id=exhibit_id)
    places = Place.objects.filter(exhibit=exhibit)
    w_es = Work_Exhibit.objects.filter(exhibit=exhibit)
    context = {'exhibit': exhibit, 'places': places, 'w_es': w_es}

    return render(request, 'core/exhibit_view.html', context)


@login_required(login_url='core:signin')
def gallery_view(request, owner_id):
    gallery = Gallery.objects.get(owner_id=owner_id)
    exhibits = Exhibit.objects.raw(
        f"SELECT * from core_exhibit where gallery_id={owner_id} and start_time>to_char(now(), 'YYYY-MM-DD') order by start_time")
    context = {'gallery': gallery, 'exhibits': exhibits}
    return render(request, 'core/gallery_view.html', context)


@login_required(login_url='core:signin')
def buy_ticket(request):
    exhibit_id = request.GET.get('exhibit_id')
    exhibit = Exhibit.objects.get(id=exhibit_id)
    exhibit.quantity_sold += 1
    exhibit.save()
    return HttpResponse('Buy successfully <a></a>')
