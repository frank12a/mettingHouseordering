from django.db import models


# Create your models here.
class Userinfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
    def __str__(self):
        return  self.user
    class Meta:
        verbose_name_plural="用户表"


class Room(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name_plural="会议室"


class Bookings(models.Model):
    user = models.ForeignKey("Userinfo")
    room = models.ForeignKey("Room")
    time_pharse = (
        (1, "8点到9点"),
        (2, "9点到10点"),
        (3, "10点到11点"),
        (4, "11点到12点"),
        (5, "14点到13点"),
        (6, "13点到14点"),
        (7, "14点到15点"),
        (8, "15点到16点"),
        (9, "16点到17点"),
        (10, "17点到18点"),
    )
    time_id = models.IntegerField(choices=time_pharse)
    date = models.DateField()
    # def __str__(self):
    #     return  self.user

    class Meta:
        unique_together =(("room", "date", "time_id"),)
        verbose_name_plural="预定情况"
