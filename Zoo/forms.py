from django import forms
from Zoo.models import Animal, Zone, Parttime, Zookeeper

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'

class ZkpForm(forms.ModelForm):
    class Meta:
        model = Zookeeper
        fields = '__all__'