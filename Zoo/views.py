from Zoo.models import Area, Zone, Animal, DetailLog, PartTime, Zookeeper
from Zoo.forms import AnimalForm, ZkpForm, DetailLogForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime


# register function
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
                return render(request, 'user/register.html', {'message': 'Passwords do not match.'})

            User.objects.create_user(username=zid, password=zpw)

        return redirect('login')

    else:
        form = ZkpForm()

    return render(request, 'user/register.html', {'form': form, 'zon': zon, 'pt': pt, 'join': join})


# login function
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
            return render(request, 'user/login.html', {'message': 'Invalid username or password.'})

    return render(request, 'user/login.html')


# logout function
def logout(request):
    # 세션에서 사용자 정보 삭제
    del request.session['username']
    return redirect('login')


# Zookeeper Page
def index(request):
    uid = request.session.get('username')
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    zid = zkp.zone.zone_id
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    zkp_list = Zookeeper.objects.filter(zone=zid).order_by("pt")
    return render(request, 'index.html',
                  {'zkp': zkp, 'zn_all': zn_all, 'area_all': area_all, 'anm_all': anm_all, 'zkp_list': zkp_list})


# Auto ID function
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


# Animal CRUD
def animal_detail(request, id): # Animal Detail Page
    uid = request.session.get('username')
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_list = Animal.objects.all().values_list('anm_id', flat=True)
    zn_list = Zone.objects.all().values_list('zone_id', flat=True)
    today = datetime.now()
    dl = DetailLog.objects.filter(anm=id).order_by('-dlog_dt')
    dl_cgr = list(set(dl.values_list('dlog_cgr', flat=True)))
    dl_count = dl.count()

    if id in anm_list:
        m = "Modify"
        anm = Animal.objects.get(pk=id)
        check_list = []
        if anm.anm_check:
            anm_last_check = anm.anm_last.date()
            if (today.date() - anm_last_check).days != 0:
                anm.anm_check = ""
            else:
                check_list = list(anm.anm_check)
        form = AnimalForm(request.POST or None, instance=anm)

        if request.method == 'POST':

            if form.is_valid():
                form.save()
                return redirect('animal_detail', id)

        return render(request, 'animal_detail.html', {'anm': anm, 'zn_all': zn_all,
                                                      'anm_list': anm_list, 'm': m, 'today': today,
                                                      'form': form, 'check_list': check_list, 'area_all': area_all,
                                                      'dl': dl, 'zkp': zkp, 'dl_cgr': dl_cgr, 'dl_count': dl_count})

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
                 'anm_last': "",
                 'anm_join': datetime.now(),
                 'zone_id': Zone.objects.get(pk=id)}
        form = AnimalForm(request.POST or None, initial=anm_1)

        if form.is_valid():
            form.save()
            return redirect('zone', id)

        return render(request, 'animal_detail.html', {'anm': anm_1, 'zn_all': zn_all,
                                                      'anm_list': anm_list, 'm': m,
                                                      'area_all': area_all, 'zkp': zkp})

    else:
        return redirect('index')


def animal_delete(request, id):
    animal = Animal.objects.get(anm_id=id)
    animal.delete()
    return redirect('index')


# check function with Animal
def check(request, id):
    anm = Animal.objects.get(pk=id)

    if request.method == 'POST':
        check_list = request.POST.getlist('checked')
        anm_check = ''.join(check_list)
        anm.anm_check = anm_check
        anm.anm_last = datetime.now()
        anm.save()
        return redirect('animal_detail', id)

    return redirect('animal_detail', id)


# search for check function
def search(request):
    uid = request.session['username']
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    return render(request, 'animal_search.html',
                  {'zkp': zkp, 'zn_all': zn_all, 'area_all': area_all, 'anm_all': anm_all})


def search_filter(request):
    uid = request.session['username']
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    anm_all = Animal.objects.all()
    anm_list = Animal.objects.all().values_list('anm_id', flat=True)
    anm = Animal.objects.all()
    now = datetime.now().time()
    meal_time = ["08:00", "13:00", "18:00"]
    feed = []
    anm_care = []
    for t in meal_time:
        t = datetime.strptime(t, "%H:%M").time()
        if now > t:
            c = meal_time.index(str(t)[0:5])+1
            feed.append(c)
            feed.append(c+3)
    anm_list_1 = anm.values_list('anm_id', 'anm_check')
    for i in anm_list_1:
        care_list = [int(i[0])]
        mc = anm_all.get(pk=int(i[0])).anm_mc
        for j in feed:
            if str(j) not in str(i[1]):
                if j == 1:
                    need = 'breakfast'
                    care_list.append(need)
                elif j == 2:
                    need = 'lunch'
                    care_list.append(need)
                elif j == 3:
                    need = 'dinner'
                    care_list.append(need)
                if mc and mc != 'Null':
                    if j == 4:
                        need = 'medicine(morning)'
                        care_list.append(need)
                    elif j == 5:
                        need = 'medicine(noon)'
                        care_list.append(need)
                    elif j == 6:
                        need = 'medicine(night)'
                        care_list.append(need)
        anm_care.append(care_list)

    return render(request, "animal_search.html", {'zkp': zkp, 'zn_all': zn_all,
                                                  'area_all': area_all, 'anm_all': anm_all,
                                                  'anm_care': anm_care, 'anm_list': anm_list})


# Log CRUD with Animal
def write_log(request, id):
    uid = request.session.get('username')
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    dl = DetailLog.objects.filter(anm=id).order_by('-dlog_dt')
    dl_cgr = list(set(dl.values_list('dlog_cgr', flat=True)))
    dl_count = dl.count()
    now = datetime.now()
    new_did = int(str(id)+'01')
    tp = "write"
    m = 'Create'
    if dl.exists():
        anm = dl.values_list('dlog_id', flat=True).order_by("-dlog_id")
        new_did = anm[0] + 1

    dlog = {'dlog_id': new_did,
            'anm': Animal.objects.get(pk=id)}

    form = DetailLogForm(request.POST or None, initial=dlog)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('animal_detail', id)

        error = form.cleaned_data
        return render(request, "write_log.html", {"form": form, "id": id, "now": now,
                                                  'error': error, 'dlog': dlog, 'type': tp, 'zn_all': zn_all,
                                                  'm': m, 'area_all': area_all, 'dl': dl, 'zkp': zkp,
                                                  'dl_cgr': dl_cgr, 'dl_count': dl_count})

    return render(request, "write_log.html", {"form": form, "id": id, "now": now, 'dlog': dlog,
                                              'type': tp, 'zn_all': zn_all, 'm': m, 'area_all': area_all,
                                              'dl': dl, 'zkp': zkp, 'dl_cgr': dl_cgr, 'dl_count': dl_count})


def edit_log(request, id):
    uid = request.session.get('username')
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
    area_all = Area.objects.all()
    zn_all = Zone.objects.all()
    dlog = DetailLog.objects.get(dlog_id=id)
    dl = DetailLog.objects.filter(anm=dlog.anm).order_by('-dlog_dt')
    dl_cgr = list(set(dl.values_list('dlog_cgr', flat=True)))
    dl_count = dl.count()
    now = datetime.now()
    dlog = DetailLog.objects.get(dlog_id=id)
    form = DetailLogForm(request.POST or None, instance=dlog)
    tp = "edit"
    m = "Modify"

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('animal_detail', dlog.anm.anm_id)

    return render(request, "write_log.html", {"form": form, "id": id, "now": now, 'dlog': dlog,
                                              'type': tp, 'zn_all': zn_all, 'm': m, 'area_all': area_all,
                                              'dl': dl, 'zkp': zkp, 'dl_cgr': dl_cgr, 'dl_count': dl_count})


def log_delete(request, id):
    dl = DetailLog.objects.get(dlog_id=id)
    anm = dl.anm
    dl.delete()
    return redirect('animal_detail', anm.anm_id)


# Zone Page
def zone(request, id):
    uid = request.session.get('username')
    if uid is None:
        message = "Plz Login First"
        return render(request, "user/404.html", {'message': message})
    uid = int(uid)
    zkp = Zookeeper.objects.get(pk=uid)
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
                'zkp_list': zkp_list,
                'zkp': zkp}

    return render(request, 'zone.html', contents)
