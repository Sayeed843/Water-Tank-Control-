from django.contrib import admin
from .models import Motor, AboutMe, DailyStatus, BdWaterBoard, Sensor
# Register your models here.
admin.site.register(Motor)
admin.site.register(AboutMe)
admin.site.register(DailyStatus)
admin.site.register(BdWaterBoard)
admin.site.register(Sensor)
