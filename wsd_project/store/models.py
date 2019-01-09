from django.db import models
from users.models import CustomUser

#games are added to the database through forms
#requires one model, one form and one view to function together
#primary key -> can't be changed afterwards, name does not need to be set as a primary key
#Game (name PRIMARY KEY, dev FOREIGN KEY, price, link, purchases, tags)
#one game can have only one developer
#how to check and limit that only developers can add a game
#->restricting only developers access to this (form creation view)view might not be enough 
#Game (name PRIMARY KEY, dev FOREIGN KEY, price, link, purchases, tags)
#how to check that the user is actually a dev?, and how to set a dev to the game?

class Game(models.Model):
    name = models.CharField(max_length = 50)
    dev = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.FloatField()
    #link = models.URLField()?????
    #purchases = models.integerField(default=0)#when adding a new game should always be set to 0
    #tags = dictionary



