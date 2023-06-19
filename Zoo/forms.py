from django import forms
from Zoo.models import Animal, Zone, PartTime, Zookeeper, CheckLog, DetailLog


class AnimalForm(forms.ModelForm):
    cleaned_data = {}

    class Meta:
        model = Animal
        fields = ['anm_id', 'anm_name', 'anm_spcs',
                  'anm_city', 'anm_sex', 'anm_old',
                  'anm_rct', 'anm_food', 'anm_mc',
                  'anm_last', 'anm_join', 'zone_id']

    def clean_anm_id(self):
        anm_id = self.cleaned_data['anm_id']
        return anm_id

    def clean_anm_name(self):
        anm_name = self.cleaned_data['anm_name']
        return anm_name

    def clean_anm_spcs(self):
        anm_spcs = self.cleaned_data['anm_spcs']
        return anm_spcs

    def clean_anm_city(self):
        anm_city = self.cleaned_data['anm_city']
        return anm_city

    def clean_anm_sex(self):
        anm_sex = self.cleaned_data['anm_sex']
        return anm_sex

    def clean_anm_old(self):
        anm_old = self.cleaned_data['anm_old']
        return anm_old

    def clean_anm_rct(self):
        anm_rct = self.cleaned_data['anm_rct']
        return anm_rct

    def clean_anm_food(self):
        anm_food = self.cleaned_data['anm_food']
        return anm_food

    def clean_anm_mc(self):
        anm_mc = self.cleaned_data['anm_mc']
        return anm_mc

    def clean_anm_check(self):
        anm_check = self.cleaned_data['anm_check']
        return anm_check

    def clean_anm_last(self):
        anm_last = self.cleaned_data['anm_last']
        return anm_last

    def clean_anm_join(self):
        anm_join = self.cleaned_data['anm_join']
        return anm_join

    def clean_anm_zone_id(self):
        zone_id = self.cleaned_data['zone_id']
        return zone_id


class ZoneForm(forms.ModelForm):
    cleaned_data = {}

    class Meta:
        model = Zone
        fields = ['zone_id', 'zone_name', 'zone_max', 'zone_loc', 'area']

    def clean_zone_id(self):
        zone_id = self.cleaned_data['zone_id']
        return zone_id

    def clean_zone_name(self):
        zone_name = self.cleaned_data['zone_name']
        return zone_name

    def clean_zone_max(self):
        zone_max = self.cleaned_data['zone_max']
        return zone_max

    def clean_zone_loc(self):
        zone_loc = self.cleaned_data['zone_loc']
        return zone_loc

    def clean_area(self):
        area = self.cleaned_data['area']
        return area


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


class DetailLogForm(forms.ModelForm):
    cleaned_data = {}

    class Meta:
        model = DetailLog
        fields = ['dlog_id', 'dlog_cgr', 'dlog_con', 'dlog_dt', 'anm']

    def clean_dlog_id(self):
        dlog_id = self.cleaned_data['dlog_id']
        return dlog_id

    def clean_dlog_cgr(self):
        dlog_cgr = self.cleaned_data['dlog_cgr']
        return dlog_cgr

    def clean_dlog_con(self):
        dlog_con = self.cleaned_data['dlog_con']
        return dlog_con

    def clean_dlog_dt(self):
        dlog_dt = self.cleaned_data['dlog_dt']
        return dlog_dt

    def clean_anm(self):
        anm = self.cleaned_data['anm']
        return anm


class CheckLogForm(forms.ModelForm):
    cleaned_data = {}

    class Meta:
        model = CheckLog
        fields = ['clog_id', 'clog_tm', 'clog_food', 'clog_bf', 'clog_lch', 'clog_dn', 'clog_mc', 'clog_mm', 'clog_lm', 'clog_em']

    def clean_clog_id(self):
        clog_id = self.cleaned_data['clog_id']
        return clog_id

    def clean_clog_tm(self):
        clog_tm = self.cleaned_data['clog_tm']
        return clog_tm

    def clean_clog_food(self):
        clog_food = self.cleaned_data['clog_food']
        if clog_food == 'None':
            clog_food = None
        return clog_food

    def clean_clog_bf(self):
        clog_bf = self.cleaned_data['clog_bf']
        return clog_bf

    def clean_clog_lch(self):
        clog_lch = self.cleaned_data['clog_lch']
        return clog_lch

    def clean_clog_dn(self):
        clog_dn = self.cleaned_data['clog_dn']
        return clog_dn

    def clean_clog_mc(self):
        clog_mc = self.cleaned_data['clog_mc']
        if clog_mc == 'None':
            clog_mc = None
        return clog_mc

    def clean_clog_mm(self):
        clog_mm = self.cleaned_data['clog_mm']
        return clog_mm

    def clean_clog_lm(self):
        clog_lm = self.cleaned_data['clog_lm']
        return clog_lm

    def clean_clog_em(self):
        clog_em = self.cleaned_data['clog_em']
        return clog_em
