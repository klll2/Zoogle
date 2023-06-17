from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from Zoo.models import Area, Zone, Animal, DetailLog, PartTime, Zookeeper
from Zoo.forms import AnimalForm, ZkpForm, DetailLogForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime, date
from django.db.models import Q


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
    zid = zkp.zone.zone_id
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    zkp_list = Zookeeper.objects.filter(zone=zid).order_by("pt")
    return render(request, 'index.html',
                  {'zkp': zkp, 'zn_all': zn_all, 'area_all': area_all, 'anm_all': anm_all, 'zkp_list': zkp_list})


def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'animal/animal_list.html', {'animals': animals})


def animal_delete(request, id):
    animal = Animal.objects.get(anm_id=id)
    animal.delete()
    return redirect('index')


def id_auto(id):
    anm_all = Animal.objects.all().values_list("anm_id", flat=True)
    if len(id) == 1:
        a_zone = Zone.objects.filter(area=id).values_list("zone_id", flat=True).order_by("-zone_id")
        auto_zone = int(a_zone[0]) + 1
        return auto_zone
    elif len(id) >= 2:
        a = []
        for i in anm_all:
            if str(i)[0:2] == id and Animal.objects.filter(zone_id=id).exists():
                a.append(i)
                a = sorted(a, reverse=True)
        if len(a) > 0:
            auto_anm = int(a[0]) + 1
            while auto_anm in anm_all:
                auto_anm += 1
        else:
            auto_anm = int(id + '1')

        return auto_anm
    else:
        return id


def zone(request, id):
    zn = Zone.objects.get(zone_id=id)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    capa = Animal.objects.filter(zone_id=id).count()
    zkp_list = Zookeeper.objects.filter(zone=id).order_by("pt")
    zkp_count = zkp_list.count()
    contents = {'zn': zn,
                'zn_all': zn_all,
                'area_all': area_all,
                'anm_all': anm_all,
                'capa': capa,
                'zkp_count': zkp_count,
                'zkp_list': zkp_list}

    return render(request, 'zone.html', contents)


def animal_detail(request, id):
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_list = Animal.objects.all().values_list('anm_id', flat=True)
    zn_list = Zone.objects.all().values_list('zone_id', flat=True)
    today = date.today()
    i = True
    dl = DetailLog.objects.filter(anm=id).order_by('dlog_id')

    if id in anm_list:
        m = "Modify"
        anm = Animal.objects.get(pk=id)
        check_list = []
        if anm.anm_check:
            check_list = list(anm.anm_check)
        form = AnimalForm(request.POST or None, instance=anm)

        if request.method == 'POST':

            if form.is_valid():
                form.save()
                return redirect('animal_detail', id)

        return render(request, 'animal_detail.html', {'anm': anm, 'zn_all': zn_all,
                                                      'anm_list': anm_list, 'm': m, 'today': today,
                                                      'form': form, 'check_list': check_list, 'i': i,
                                                      'area_all': area_all, 'dl': dl})

    elif id in zn_list:
        m = "Create"
        anm_list = Animal.objects.all().values_list("anm_id", flat=True)
        new_id = id_auto(str(id))
        anm_1 = {'anm_id': new_id,
                 'anm_name': "",
                 'anm_spcs': "",
                 'anm_city': "",
                 'anm_sex': "",
                 'anm_old': "",
                 'anm_rct': "",
                 'anm_food': "",
                 'anm_mc': "",
                 'anm_check': "",
                 'zone_id': Zone.objects.get(pk=id)}
        form = AnimalForm(request.POST or None, initial=anm_1)

        if form.is_valid():
            form.save()
            return redirect('zone', id)

        return render(request, 'animal_detail.html', {'anm': anm_1, 'zn_all': zn_all,
                                                      'anm_list': anm_list, 'm': m,
                                                      'area_all': area_all})

    else:
        return redirect('index')


def check(request, id):
    anm = Animal.objects.get(pk=id)

    if request.method == 'POST':
        check_list = request.POST.getlist('checked')
        anm_check = ''.join(check_list)
        anm.anm_check = anm_check
        anm.save()
        return redirect('animal_detail', id)

    return redirect('animal_detail', id)


def write_log(request, id):
    now = datetime.now()
    new_did = int(str(id)+'01')
    tp = "write"
    if DetailLog.objects.filter(anm=id).exists():
        anm = DetailLog.objects.filter(anm=id).values_list('dlog_id', flat=True).order_by("-dlog_id")
        new_did = anm[0] + 1

    dl_1 = {'dlog_id': new_did,
            'anm': Animal.objects.get(pk=id)}

    form = DetailLogForm(request.POST or None, initial=dl_1)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('animal_detail', id)

        error = form.cleaned_data
        return render(request, "write_log.html", {"form": form, "id": id, "now": now,
                                                  'error': error, 'dl': dl_1, 'type': tp})

    return render(request, "write_log.html", {"form": form, "id": id, "now": now, 'dl': dl_1, 'type': tp})


def edit_log(request, id):
    now = datetime.now()
    dl = DetailLog.objects.get(dlog_id=id)
    form = DetailLogForm(request.POST or None, instance=dl)
    tp = "edit"

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('animal_detail', dl.anm.anm_id)

    return render(request, "write_log.html", {"form": form, "id": id, "now": now, 'dl': dl, 'type': tp})


def log_delete(request, id):
    dl = DetailLog.objects.get(dlog_id=id)
    anm = dl.anm
    dl.delete()
    return redirect('animal_detail', anm.anm_id)



