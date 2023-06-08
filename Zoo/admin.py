from django.contrib import admin
from .models import Area, Zone, Animal, CheckLog, DetailLog, PartTime, Zookeeper

admin.site.register(Area)
admin.site.register(Zone)
admin.site.register(Animal)
admin.site.register(CheckLog)
admin.site.register(DetailLog)
admin.site.register(PartTime)
admin.site.register(Zookeeper)


