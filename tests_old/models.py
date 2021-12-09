from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Schmidt'

doc = """
Explains Experiment and asks some test questions
"""


class Constants(BaseConstants):
    name_in_url = 'tests'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    num_participants = models.IntegerField(label="how many?", initial=1)


class Player(BasePlayer):
    test_questions1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_questions2 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_points1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_points2 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_slider1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_slider2 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)

    # safes number of mistakes
    mistakes = models.IntegerField(initial=0)

    example_slider = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")
    example_slider1 = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")
    example_slider2 = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")
    example_slider3 = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")

    test_all1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_all2 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_all3 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)
    test_all4 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)