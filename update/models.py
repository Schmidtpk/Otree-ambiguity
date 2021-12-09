from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


import itertools
import random



author = 'Patrick Schmidt'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'update'
    players_per_group = None
    num_rounds = 4
    # minutes in topic before time out
    minutes = 5
    # safes all types of elicitation in dynamic page
    elicit_types = ["choice", "ticket", "slider"]
    a = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    ]
    q = [
        5,
        1,
        9,
        3,
        7,
    ]
    dynamic_question_number = 5

    # Title at the top of each page
    title_all = [
        "Weniger als 10?",
        "Mehr als 20?",
        "Weniger als 10? (2. Runde)",
        "Mehr als 20? (2. Runde)",
    ]

    # Text used to explain the domain at explanation page
    explaintext_all = [
        "Wir betrachten, ob weniger oder mehr als 10 rote Bälle in der Urne sind.",
        "Wir betrachten, ob weniger oder mehr als 20 rote Bälle in der Urne sind.",
        "Wir betrachten, ob weniger oder mehr als 10 rote Bälle in der Urne sind.",
        "Wir betrachten, ob weniger oder mehr als 20 rote Bälle in der Urne sind.",
    ]
    # Short summary of event
    ctext_short_all = [
            "10 bis 30",
            "21 bis 30",
            "10 bis 30",
            "21 bis 30",
            ]
    # Short summary of complement
    etext_short_all = [
        "0 bis 9",
        "0 bis 20 ",
        "0 bis 9",
        "0 bis 20 ",
    ]
    # Text used to describe the event
    ctext_all = [
            "es 10 bis 30 rote Bälle sind",
            "es 21 bis 30 rote Bälle sind",
            "es 11 bis 30 rote Bälle sind",
            "es 21 bis 30 rote Bälle sind",
    ]
    # Text used to describe the complement
    etext_all = [
            "es 0 bis 9 rote Bälle sind",
            "es 0 bis 20 rote Bälle sind",
            "es 0 bis 9 rote Bälle sind",
            "es 0 bis 20 rote Bälle sind",
    ]
    # Text used to describe to desribe independence
    mtext_all = [
        "wieviele rote Bälle in der Urne sind",
        "wieviele rote Bälle in der Urne sind",
        "wieviele rote Bälle in der Urne sind",
        "wieviele rote Bälle in der Urne sind",
    ]

    text_choice = "Was bevorzugen Sie?"

    def make_field(label):
        return models.StringField(
            label=label,
            widget=widgets.RadioSelect,
            blank=True,
        )

    def make_fieldt():
        return models.IntegerField(min=0, max=100, blank=True)


    # makes text for choice page in dynamic context
    def make_text_dynamic(self):
        print("In text making q is:", self.player.q_now)
        return [['M',
                 str(self.player.q_now * (10 - self.player.q_now)) +
                 " Punkte sicher, egal " +
                 Constants.mtext[self.round_number-1]
                 ]
                ,
                ['E',
                 str(self.player.q_now * 10) +
                 ' Punkte, nur falls ' +
                 Constants.etext[self.round_number - 1]
                ]
                ,
                ['C',
                 str((10 - self.player.q_now) * 10) +
                 ' Punkte, nur falls ' +
                 Constants.ctext[self.round_number - 1]
                ]
                ]

    # defines text for ticketsPage label
    def make_labelt(self, q):
        return Constants.etext[self.round_number-1] +\
            ", erhalten Sie " +\
            str((10-Constants.a[q])*10) +\
            "% dieser Punkte."

    # defines text for ticketsPage on the right side
    def make_labeltb(self, q):
        return Constants.ctext[self.round_number-1] +\
            ", erhalten Sie " +\
            str((Constants.a[q]) * 10) +\
            "% dieser Punkte."

    def extract(loc_list):
        return [loc_list[i] for i in [0, 1, 2, 3]]

    title = extract(title_all)
    explaintext = extract(explaintext_all)
    ctext_short = extract(ctext_short_all)
    etext_short = extract(etext_short_all)
    mtext = extract(mtext_all)
    ctext = extract(ctext_all)
    etext = extract(etext_all)


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        treatments = itertools.cycle([1, 2, 3])
        for p in self.get_players():
            p.treatment = next(treatments)


class Group(BaseGroup):
    eventTRUE10 = models.BooleanField()
    eventTRUE20 = models.BooleanField()
    eventTRUE1020 = models.BooleanField()
    title = models.StringField()
    red_draws = models.IntegerField()

class Player(BasePlayer):

    # treatments
    treatment = models.IntegerField()
    prize = models.StringField()

    # payoff
    payoffq = models.IntegerField()
    x = models.FloatField()

    input = models.IntegerField(label="True number?")

    # safes number of red draws in update
    input_update = models.IntegerField(label="Number of red draws?")

    # ------ Money reward assignment
    def random_money_assignment(self):
        # randomize to treatments
        cur_random = random.choice([10])
        print("Random treatment assignment of ", cur_random)
        self.prize = cur_random


    # safes input
    val_now = Constants.make_field(Constants.text_choice)
    # safes intern round in dynamic page
    dyn_round = models.IntegerField()
    # safes position for which mixing is irrational below
    mix_lower = models.IntegerField(initial=0)
    # safes position for which mixing is irrational above
    mix_upper = models.IntegerField(initial=10)
    # safes if dynamic already finished
    dynamic_end = models.BooleanField(initial=False)
    # safes current q
    q_now = models.IntegerField(initial=5)
    # safes counter for which results are shown
    results_counter = models.IntegerField(initial=0)
    # safes question order
    choices_order = models.LongStringField(initial="O")
    # safes all input
    dyn_all = models.StringField(initial="S")

    # safes current elicitation type
    elicit_type = models.StringField()

    # safes ticket dyn output
    val_ticket = Constants.make_fieldt()
    valtdyn = Constants.make_fieldt()
    valtdynb = Constants.make_fieldt()

    # safes slider dyn output
    val_slider_dyn = models.IntegerField(widget=widgets.Slider(attrs={'step': '1'}, show_value=False),
                                         label="",
                                         blank=True)
    # safes if slider was moved for error message
    moved_slider = models.IntegerField(initial=0, blank=True)

    # returns right q in dynamic page
    def get_q_now(self):
        print("lower now:", self.mix_lower)
        print("upper now:", self.mix_upper)
        for i in range(self.dyn_round, Constants.dynamic_question_number):
            if self.mix_lower < self.participant.vars['q'][i] < self.mix_upper:
                self.dyn_round = i + 1
                print("Update dyn_round to", self.dyn_round)
                return self.participant.vars['q'][i]
        print("For loop is over")
        self.dynamic_end = True
        return 99


    def tickets_text_dyn_E(self):
        return(
            Constants.etext[self.round_number - 1] + \
            ", erhalten Sie " + \
            str(self.q_now * 10) + \
            "% dieser Punkte."
        )

    def tickets_text_dyn_C(self):
        return(
            Constants.ctext[self.round_number - 1] + \
            ", erhalten Sie " + \
            str((10 - self.q_now) * 10) + \
            "% dieser Punkte."
        )


    # methods to put text in templates
    def fun_title(self):
        return(Constants.title[self.round_number-1])
    def etext_short(self):
        return(Constants.etext_short[self.round_number-1])
    def ctext_short(self):
        return(Constants.ctext_short[self.round_number-1])
    def fun_etext(self):
        return(Constants.etext[self.round_number-1])
    def fun_ctext(self):
        return(Constants.ctext[self.round_number-1])
    def fun_explanation(self):
        return(Constants.explaintext[self.round_number-1])
    def result_event(self):
        return(Constants.results[self.round_number-1])
    def winning_chance(self):
        return(round(100*(Constants.a[self.payoffq]/10 * self.x * self.group.eventTRUE +
               (1-Constants.a[self.payoffq]/10) * (1-self.x) * (1-self.group.eventTRUE))))
    def number_selected_bet(self):
        return(self.payoffq+1)

    def tickets_prize_text(self):
        return(str(self.prize)+" Euro")
