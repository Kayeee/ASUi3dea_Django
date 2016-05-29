import datetime

from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import geohash
import re
# Create your models here.

@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    REQUIRED_FIELDS = ('user',)
    USERNAME_FIELD = ('username')

    def __str__(self):
        return u'Profile of user: %s' % self.user.username

@python_2_unicode_compatible
class InverterGroup(models.Model):
    name = models.CharField(max_length=30, default = "")
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} owns this group ({1})".format(self.owner, self.name)

@python_2_unicode_compatible
class Pi(models.Model):
    latitude = models.FloatField(default = 33.3059398)
    longitude = models.FloatField(default = -111.6792469)
    id = models.CharField(max_length=30, primary_key=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.id = geohash.encode(self.latitude, self.longitude, 24)
            print('geohash: {0}'.format(self.id))
        super(Pi, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

@python_2_unicode_compatible
class Inverter(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE)
    sunspecid = models.IntegerField(default = -1)
    SunSpecDID = models.IntegerField(default = -1)
    Manufacturer = models.CharField(max_length=20, default="-1")
    Model = models.CharField(max_length=20, default="-1")
    Version = models.CharField(max_length=20, default="-1")
    SerialNumber = models.IntegerField(default = -1)
    DeviceAddress = models.IntegerField(default = -1)
    SunSpecDIDphase = models.CharField(max_length=20, default="-1")
    groups = models.ManyToManyField(InverterGroup, editable = False)
    custom_name = models.CharField(max_length=30, default = "", blank=True)
    id = models.CharField(editable = False, max_length=255, primary_key=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            invert_family = self.__class__.objects.filter(pi_id=self.pi.id)#all inverters conected to the same pi
            if invert_family:
                stripped_inverter_id = [re.sub(r'(.*)-', '', str(i.id)) for i in invert_family]
                stripped_inverter_id.sort(reverse=True)
                self.id = self.pi.id + '-' + str(int(stripped_inverter_id[0]) + 1)
            else:
                self.id = self.pi.id + '-0'

        if self.custom_name is "":
            self.custom_name = self.id
        super(Inverter, self).save(*args, **kwargs)

    def is_on(self):
        return self.state

    def non_foreign_attribs(self):
        return ['pi', 'sunspecid', 'SunSpecDID', 'Manufacturer', 'Model', 'Version', 'SerialNumber', 'DeviceAddress', 'SunSpecDIDphase', 'pi_id']

    def __str__(self):
        return self.id

#Ambient Temperature
class Temperature(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    temperature = models.FloatField(default = 0)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "Temperature")
    def get_data(self):
        return (self.timestamp, self.temperature)
    def set_data(self, new_temp):
        self.temperature = new_temp

#I-Status
class Status(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    status = models.IntegerField(default = -1)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "Status")
    def get_data(self):
        return (self.timestamp, self.status)
    def set_data(self, new_status):
        self.status = new_status

class Mode(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    on_off = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "Mode")
    def get_data(self):
        return (self.timestamp, self.on_off)
    def set_data(self, new_mode):
        self.on_off = new_mode

@python_2_unicode_compatible
class Address(models.Model):
    pi = models.ForeignKey(Pi, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=20, default = "")
    street = models.CharField(max_length=50, default="")
    zipcode = models.IntegerField(default=0)
    # def save(self, *args, **kwargs):
    #     if not self.pk:  # object is being created, thus no primary key field yet
    #         #Need to create address parser here possibly.
    #     super(Pi, self).save(*args, **kwargs)
    def __str__(self):
        return "{0}\n{1},{2} {3}".format(self.street, self.city, self.state, str(self.zipcode))

@python_2_unicode_compatible
class HeatSinkTemp(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    temperature = models.FloatField(default = -1)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "HeatSinkTemp")
    def get_data(self):
        return (self.timestamp, self.temperature)
    def set_data(self, new_temp):
        self.temperature = new_temp
    def __str__(self):
        return "Time: {0}, Value: {1}".format(self.timestamp, self.temperature)

@python_2_unicode_compatible
class ACPower(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    power = models.FloatField(default = -1)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "AC_Power")
    def get_data(self):
        return (self.timestamp, self.power)
    def set_data(self, new_power):
        self.power = new_power
    def __str__(self):
        return "Time: {0}, Value: {1}".format(self.timestamp, self.power)


@python_2_unicode_compatible
class DCPower(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    power = models.FloatField(default = -1)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "DC_Power")
    def get_data(self):
        return (self.timestamp, self.power)
    def set_data(self, new_power):
        self.power = new_power
    def __str__(self):
        return "Time: {0}, Value: {1}".format(self.timestamp, self.power)

@python_2_unicode_compatible
class ACEnergyWH(models.Model):
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE)
    watt_hours = models.FloatField(default = -1)
    timestamp = models.DateTimeField(auto_now_add=True)
    generic_name = models.CharField(max_length=20, default = "AC_Energy_WH")
    def get_data(self):
        return (self.timestamp, self.watt_hours)
    def set_data(self, new_watt_hours):
        self.watt_hours = new_watt_hours
    def __str__(self):
        return "Time: {0}, Value: {1}".format(self.timestamp, self.watt_hours)
