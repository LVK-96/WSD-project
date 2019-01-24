from django.db import models
from users.models import CustomUser


#primary key -> can't be changed afterwards, name does not need to be set as a primary key

class Game(models.Model):
    name = models.CharField(max_length=50)
    #should this be CustomUser or profile
    dev = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    link = models.URLField(unique=True, default="")
    #purchases = models.integerField(default=0)#when adding a new game should always be set to 0
    #tags = dictionary

class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, unique=False)

class Order(models.Model):
    #buyer 
    player = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    #bought games 
    games = models.ManyToManyField(Game, default=None, blank=True)
    total = models.FloatField(default=0, null=False)