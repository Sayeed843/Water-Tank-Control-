from django.db import models
from datetime import datetime

# Create your models here.


class BdWaterBoard(models.Model):
    user = models.CharField(max_length=250)
    mac = models.CharField(max_length=250)
    gallon = models.CharField(max_length=250)
    use = models.CharField(max_length=250, default=0)
    remaining = models.CharField(max_length=250, default=0)

    def __str__(self):
        return self.user


class Motor(models.Model):
    mac_fk = models.ForeignKey(BdWaterBoard, on_delete=models.CASCADE)
    waterSupply = models.BooleanField()

    def __str__(self):
        return str(self.mac_fk)


# class Sensor(models.Model):
#     mac = models.ForeignKey(BdWaterBoard, on_delete=models.CASCADE)
#     upperSensor = models.CharField(max_length=250)
#     lowerSensor = models.CharField(max_length=250)
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#
#     def __str__(self):
#         return str(self.mac)


class Sensor(models.Model):
    mac = models.ForeignKey(BdWaterBoard, on_delete=models.CASCADE,)
    upperSensor = models.CharField(max_length=260)
    lowerSensor = models.CharField(max_length=260)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.mac)


class DailyStatus(models.Model):
    mac_id = models.ForeignKey(BdWaterBoard, on_delete=models.CASCADE,)
    motorStatus = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.mac_id) + " - " + str(self.motorStatus) + " - " + "Time: " + str(self.time)
        # return (self.motorStatus)


class AboutMe(models.Model):
    name = models.CharField(max_length=250)
    dept = models.CharField(max_length=250)
    university = models.CharField(max_length=250)
    batch = models.CharField(max_length=250)
    img = models.ImageField(blank=True)

    def __str__(self):
        return self.name
