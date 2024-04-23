from django.db import models

class data(models.Model):
    name = models.CharField(max_length=999,default="New Data")
    value = models.CharField(max_length=999999)
    
    def __str__(self):
        return "ID: " + str(self.id) + " VALUE: " + str(self.value)