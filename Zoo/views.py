from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from Zoo.models import Area, Zone, Animal, CheckLog, DetailLog, Parttime, Zookeeper
from Zoo.forms import AnimalForm, ZkpForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the password and confirm password match
        if password != confirm_password:
            return render(request, 'create_user.html', {'error': 'Passwords do not match.'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'create_user.html', {'error': 'Username already exists.'})

        # Create a new user
        User.objects.create_user(username=username, password=password)

        return redirect('login')

    return render(request, 'create_user.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            return redirect('animal_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')
def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'animal/animal_list.html', {'animals' : animals})


def animal_create(request):
    form = AnimalForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('animal_list')

    return render(request, 'animal/animal_form.html', {'form': form})


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
