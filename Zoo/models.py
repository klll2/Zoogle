from django.db import models
import datetime
# Create your models here.


class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=20)
    area_loc = models.CharField(max_length=45)


class PartTime(models.Model):
    pt_id = models.IntegerField(primary_key=True)
    pt_name = models.CharField(max_length=20)
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
    zkp_pw = models.CharField(max_length=50)
    zkp_cpw = models.CharField(max_length=50)
    zkp_name = models.CharField(max_length=11)
    zkp_call = models.CharField(max_length=11)
    zkp_carr = models.CharField(max_length=10)
    zkp_join = models.DateTimeField()
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    pt = models.ForeignKey('PartTime', on_delete=models.CASCADE)


class Animal(models.Model):
    anm_id = models.IntegerField(primary_key=True)
    anm_name = models.CharField(max_length=45)
    anm_spcs = models.CharField(max_length=45)
    anm_city = models.CharField(max_length=45)
    anm_sex = models.CharField(max_length=20)
    anm_old = models.IntegerField(blank=True, null=True)
    anm_rct = models.CharField(max_length=45)
    anm_food = models.CharField(max_length=20, blank=True, null=True)
    anm_mc = models.CharField(max_length=20, default='Null')
    anm_check = models.CharField(max_length=10, blank=True, null=True)
    anm_last = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    anm_join = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    zone_id = models.ForeignKey('Zone', on_delete=models.CASCADE)


class DetailLog(models.Model):
    dlog_id = models.IntegerField(primary_key=True)
    dlog_cgr = models.CharField(max_length=20)
    dlog_con = models.CharField(max_length=100)
    dlog_dt = models.DateTimeField()
    anm = models.ForeignKey('Animal', on_delete=models.CASCADE)



