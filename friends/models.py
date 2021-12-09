from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'friends'
    players_per_group = None
    num_rounds = 1

    # determine choice of topic and round for payoff
    # (is safed in explanations and used after each dyn page)
    payoff_topic = "Ball aus Urne"
    payoff_num = 2


class Subsession(BaseSubsession):

    def creating_session(self):
        self.session.vars['num_players'] = 0



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(label="Dein Vorname:")

