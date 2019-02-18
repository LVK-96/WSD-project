from django.db import models
from users.models import CustomUser
import json
#primary key -> can't be changed afterwards, name does not need to be set as a primary key

class Game(models.Model):
    name = models.CharField(max_length=50)
    #should this be CustomUser or profile
    dev = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    link = models.URLField(unique=True, default="", null=False)
    description = models.CharField(default='', max_length=1000)
    #purchases = models.integerField(default=0)#when adding a new game should always be set to 0
    #tags = dictionary

class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, unique=False)
    state = models.TextField(default="")
    class Meta:
        unique_together = ('game', 'player')

class Order(models.Model):
    # Choices for status
    OPENED_PAYMENT = 'OP'
    ACCEPTED_PAYMENT = 'AP'
    CANCELED_PAYMENT = 'CAN'
    SUCCESFULL_PAYMENT = 'SUC'
    FAILED_PAYMENT = 'FAI'
    STATUS_CHOICES = (
        (OPENED_PAYMENT, "Proceeded to pay"),
        (ACCEPTED_PAYMENT, "Accepted payment"),
        (CANCELED_PAYMENT, "Canceled payment"),
        (SUCCESFULL_PAYMENT, "Succesfull payment"),
        (FAILED_PAYMENT, "Failed payment"),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(choices = STATUS_CHOICES, default=OPENED_PAYMENT, max_length=20)
    games = models.ManyToManyField(Game)
    session_key = models.CharField(max_length=500)
    total = models.FloatField(default=0, null=False)
    games_and_prices = models.TextField()
    date = models.DateTimeField(auto_now=True)
    total = models.FloatField(default=0, null=False)

    def encodeJSON(self, games_prices_dict):
        json_string = json.dumps(games_prices_dict)
        return json_string

    def decodeJSON(self, json_string):
        decoded = json.loads(json_string)
        return decoded
