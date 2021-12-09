from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'IP'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    qsrcloudquestion1 = models.FloatField(label = "")
    qsrcloudquestion2 = models.FloatField(label = "")
    qsrcloudquestion3 = models.FloatField(label = "")
    qsrcloudquestion4 = models.FloatField(label = "")
    int1 = models.IntegerField()
    int2 = models.IntegerField()
    int3 = models.IntegerField()
    int4 = models.IntegerField()
