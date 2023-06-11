from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from Zoo.models import Area, Zone, Animal, CheckLog, DetailLog, PartTime, Zookeeper
from Zoo.forms import AnimalForm, ZkpForm, ZoneForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime


def user_create(request):

    zon = sorted(Zone.objects.all().values_list('zone_id', 'zone_name'))
    pt = sorted(PartTime.objects.all().values_list('pt_id', 'pt_name'))
    join = datetime.now()

    if request.method == 'POST':
        form = ZkpForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            form.instance.zkp_id = cleaned_data['zkp_id']
            form.instance.zkp_pw = cleaned_data['zkp_pw']
            form.instance.zkp_cpw = cleaned_data['zkp_cpw']
            form.instance.zkp_name = cleaned_data['zkp_name']
            form.instance.zkp_call = cleaned_data['zkp_call']
            form.instance.zkp_carr = cleaned_data['zkp_carr']
            form.instance.zkp_join = cleaned_data['zkp_join']
            form.instance.zone = cleaned_data['zone']
            form.instance.pt = cleaned_data['pt']
            form.save()

            zid = cleaned_data['zkp_id']
            zpw = cleaned_data['zkp_pw']
            cpw = cleaned_data['zkp_cpw']

            if zpw != cpw:
                Zookeeper.objects.filter(zkp_pw=zpw, zkp_cpw=cpw).delete()
                return render(request, 'register.html', {'message': 'Passwords do not match.'})

            User.objects.create_user(username=zid, password=zpw)

        return redirect('login')

    else:
        form = ZkpForm()

    return render(request, 'register.html', {'form': form, 'zon': zon, 'pt': pt, 'join': join})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            auth.login(request, user)
            request.session['username'] = user.username
            return redirect('index')
        else:
            return render(request, 'login2.html', {'message': 'Invalid username or password.'})

    return render(request, 'login2.html')


def logout(request):
    # 세션에서 사용자 정보 삭제
    del request.session['username']
    return redirect('login')


def index(request):
    uid = request.session['username']
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    return render(request, 'index.html', {'zkp': zkp, 'zn_all': zn_all, 'area_all': area_all, 'anm_all': anm_all})


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
        z = Zone.objects.filter(area_id=id).count() + 1
        zone_auto = str(id) + str(z)
        zone_auto.replace(" ", "")
        return zone_auto
    elif Zone.objects.filter(zone_id=id).count() > 0:
        a = Animal.objects.filter(zone_id=id).count() + 1
        anm_auto = str(id) + str(a)
        anm_auto.replace(" ", "")
        return anm_auto
    else:
        return id


def zone(request, id):
    zn = Zone.objects.get(zone_id=id)
    form = ZoneForm(request.POST or None, instance=zn)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()

    if form.is_valid():
        form.save()
        return redirect('zone_list')

    return render(request, 'zone.html', {'form': form, 'zn': zn, 'zn_all': zn_all, 'area_all': area_all})
