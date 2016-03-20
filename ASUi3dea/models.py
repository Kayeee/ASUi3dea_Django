import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import geohash
import re
# Create your models here.

class Pi(models.Model):
    latitude = models.FloatField(default = 33.3059398)
    longitude = models.FloatField(default = -111.6792469)
    id = models.CharField(max_length=30, primary_key=True, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.id = geohash.encode(self.latitude, self.longitude, 30)
            print('geohash: {0}'.format(self.id))
        super(Pi, self).save(*args, **kwargs)


class Inverter(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE)
    state = models.BooleanField(default = False)
    temp = models.FloatField(default = 0)
    on_time = models.IntegerField(default = 0)
    latitude = models.FloatField(default = 33.3059398)
    longitude = models.FloatField(default = -111.6792469)
    id = models.CharField(max_length=30, primary_key=True, default=None)

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # object is being created, thus no primary key field yet
    #         invert_family = self.__class__.objects.filter(pi_id=self.pi.id)#all inverters conected to the same pi
    #         stripped_inverter_id = [re.sub(r'(.*)-', '', i) for i in invert_family]
    #         last_id =  self.__class__.objects.all().order_by("-id")[0].id
    #         if last_id is not None:
    #
    #     super(Inverter, self).save(*args, **kwargs)

    def is_on(self):
        return self.state

class Temperature(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    temperature = models.FloatField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "Temperature")
    def get_data(self):
        return (self.timestamp, self.temperature)

class Mode(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    on_off = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "Mode")
    def get_data(self):
        return (self.timestamp, self.on_off)

# class Voltage(models.Model):
#     inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
#     voltage = models.FloatField(default = 0)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     generic_name = models.CharField(max_length=20, default = "Voltage")
#     def get_data(self):
#         return (self.timestamp, self.voltage)
#
# class PowerQuality(models.Model):
#     inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
#     power_quality = models.CharField(max_length=20, default = "Good")
#     timestamp = models.DateTimeField(auto_now_add=True)
#     generic_name = models.CharField(max_length=20, default = "PowerQuality")
#     def get_data(self):
#         return (self.timestamp, self.power_quality)
#
# class Current(models.Model):
#     inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
#     current = models.FloatField(default = 0)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     generic_name = models.CharField(max_length=20, default = "Current")
#     def get_data(self):
#         return (self.timestamp, self.current)
#
# class Wattage(models.Model):
#     inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
#     wattage = models.FloatField(default = 0)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     generic_name = models.CharField(max_length=20, default = "Wattage")
#     def get_data(self):
#         return (self.timestamp, self.wattage)
#
# class Frequency(models.Model):
#     inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
#     frequency = models.FloatField(default = 0)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     generic_name = models.CharField(max_length=20, default = "Frequency")
#     def get_data(self):
#         return (self.timestamp, self.frequency)
