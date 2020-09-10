from django.db import models

# Create your models here.

class Transaction(models.Model):
    brought_from = models.CharField(max_length=50)
    sold_to = models.CharField(max_length=50)
    quantity = models.IntegerField()
    c_rate = models.FloatField()
    s_rate = models.FloatField()
    cp = models.FloatField()
    sp = models.FloatField()
    profit = models.FloatField()
    
    def __str__(self):
        return str(self.id) + self.brought_from