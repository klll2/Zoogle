from django import forms
from Zoo.models import Animal, Zone, PartTime, Zookeeper


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'


class ZkpForm(forms.ModelForm):
    cleaned_data = {}

    class Meta:
        model = Zookeeper
        fields = ['zkp_id', 'zkp_pw', 'zkp_cpw', 'zkp_name', 'zkp_call', 'zkp_carr', 'zkp_join', 'zone', 'pt']

    def clean_zkp_id(self):
        zkp_id = self.cleaned_data['zkp_id']
        return zkp_id

    def clean_zkp_pw(self):
        zkp_pw = self.cleaned_data['zkp_pw']
        return zkp_pw

    def clean_zkp_cpw(self):
        zkp_cpw = self.cleaned_data['zkp_cpw']
        return zkp_cpw

    def clean_zkp_name(self):
        zkp_name = self.cleaned_data['zkp_name']
        return zkp_name

    def clean_zkp_call(self):
        zkp_call = self.cleaned_data['zkp_call']
        return zkp_call

    def clean_zkp_carr(self):
        zkp_carr = self.cleaned_data['zkp_carr']
        return zkp_carr

    def clean_zkp_join(self):
        zkp_join = self.cleaned_data['zkp_join']
        return zkp_join

    def clean_zone(self):
        zone = self.cleaned_data['zone']
        return zone

    def clean_pt(self):
        pt = self.cleaned_data['pt']
        return pt
