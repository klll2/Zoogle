from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from Zoo.models import Area, Zone, Animal, CheckLog, DetailLog, PartTime, Zookeeper
from Zoo.forms import AnimalForm, ZkpForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def create_user(request):
    form = ZkpForm(request.POST or None)
    zone = Zone.objects.all().values_list('zone_id')
    pt = PartTime.objects.all().values_list('pt_id')

    if request.method == 'POST':
        # need to fix username = request.POST
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the password and confirm password match
        if password != confirm_password:
            return render(request, 'create_user.html', {'error': 'Passwords do not match.'})

        # Create a new user
        User.objects.create_user(username=z, password=password)

        return redirect('login')

    if form.is_valid():
        form.save()

    return render(request, 'create_user.html', {'form': form, 'zone': zone, 'pt': pt})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            un = int(username)
            zkp = Zookeeper.objects.get(pk=un)
            return render(request, 'main.html', {'zkp': zkp})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')


def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'animal/animal_list.html', {'animals': animals})


def animal_create(request):
    form_auto = id_auto(id=11)
    i = {'anm_id': form_auto}
    form = AnimalForm(request.POST or None, initial=i)

    if form.is_valid():
        form.save()
        return redirect('animal_list')

    return render(request, 'animal/animal_form.html', {'form': form, 'form_auto': form_auto})


def animal_update(request, id):
    animal = Animal.objects.get(anm_id=id)
    form = AnimalForm(request.POST or None, instance=animal)

    if form.is_valid():
        form.save()
        return redirect('animal_list')

    return render(request, 'animal/animal_form.html', {'form': form, 'animal': animal})


def animal_delete(request, id):
    animal = Animal.objects.get(anm_id=id)

    if request.method == 'POST':
        animal.delete()
        return redirect('animal_list')

    return render(request, 'animal/animal_delete_confirm.html', {'animal': animal})


def id_auto(id):
    if Area.objects.filter(area_id=id).count() > 0:
        z = Zone.objects.filter(area_id=id).count()+1
        zone_auto = str(id)+str(z)
        zone_auto.replace(" ", "")
        return zone_auto
    elif Zone.objects.filter(zone_id=id).count() > 0:
        a = Animal.objects.filter(zone_id=id).count()+1
        anm_auto = str(id)+str(a)
        anm_auto.replace(" ", "")
        return anm_auto
    else:
        return id



