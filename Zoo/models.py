from django.db import models

# Create your models here.

class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=20)
    area_loc = models.CharField(max_length=45)

class Parttime(models.Model):
    pt_id = models.IntegerField(primary_key=True)
    pt_name = models.IntegerField()
    pt_start = models.TimeField()
    pt_end = models.TimeField()

class Zone(models.Model):
    zone_id = models.IntegerField(primary_key=True)
    zone_name = models.CharField(max_length=20)
    zone_max = models.IntegerField()
    zone_loc = models.CharField(max_length=45)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)

class Zookeeper(models.Model):
    zkp_id = models.IntegerField(primary_key=True)
    zkp_name = models.CharField(max_length=11)
    zkp_call = models.CharField(max_length=11)
    zkp_carr = models.CharField(max_length=10)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    pt = models.ForeignKey('Parttime', on_delete=models.CASCADE)

class Animal(models.Model):
    anm_id = models.IntegerField(primary_key=True)
    anm_name = models.CharField(max_length=45)
    anm_spcs = models.CharField(max_length=45)
    anm_city = models.CharField(max_length=45)
    anm_sex = models.CharField(max_length=20)
    anm_birth = models.DateField(blank=True, null=True)
    anm_rct = models.CharField(max_length=45)
    anm_img = models.TextField(blank=True, null=True)
    zone_id = models.ForeignKey('Zone', on_delete=models.CASCADE)

class DetailLog(models.Model):
    dlog_id = models.IntegerField(primary_key=True)
    dlog_cgr = models.CharField(max_length=20)
    dlog_con = models.CharField(max_length=100)
    dlog_dt = models.DateTimeField()
    anm_id = models.ForeignKey('Animal', on_delete=models.CASCADE)

class CheckLog(models.Model):
    anm_id = models.OneToOneField('Animal', on_delete=models.CASCADE, primary_key=True)
    clog_tm = models.TimeField()
    clog_food = models.CharField(max_length=45)
    clog_bf = models.IntegerField()
    clog_lch = models.IntegerField()
    clog_dn = models.IntegerField()
    clog_mc = models.CharField(max_length=45, blank=True, null=True)
    clog_mm = models.IntegerField(blank=True, null=True)
    clog_lm = models.IntegerField(blank=True, null=True)
    clog_em = models.IntegerField(blank=True, null=True)

