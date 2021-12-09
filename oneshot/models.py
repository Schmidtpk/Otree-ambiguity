from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Patrick Schmidt'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'oneshot'
    players_per_group = None
    num_rounds = 1


    # minutes in topic before time out
    minutes = 2
    # safes all types of elicitation in dynamic page
    elicit_types = ["choice"]
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
        4,
        5,
        6,
    ]
    dynamic_question_number = 1

    # Title at the top of each page
    title_all = [
             "Ball aus Urne",
    ]

    # Text used to explain the domain at explanation page
    explaintext_all = [
        "Ein Teilnehmer hat 10 Bälle in eine Urne gelegt. Die Bälle sind blau und rot. Die Anzahl an blauen und roten Bällen in der Urne konnte der Teilnehmer frei wählen und ist geheim. Nun wird der Teilnehmer blind einen Ball aus der Urne ziehen.",
    ]
    # Short summary of event
    ctext_short_all = [
        "blauer Ball",
    ]
    # Short summary of complement
    etext_short_all = [
        "roter Ball",
    ]
    # Text used to describe the event
    ctext_all = [
            "ein blauer Ball gezogen wird",
    ]
    # Text used to describe the complement
    etext_all = [
        "ein roter Ball gezogen wird",
    ]
    # Text used to describe to desribe independence
    mtext_all = [
        "was für ein Ball gezogen wird",
    ]
    text_choice = "Was bevorzugen Sie?"

    def make_field(label):
        return models.StringField(
            label=label,
            widget=widgets.RadioSelect,
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
                 ' Punkte, falls ' +
                 Constants.etext[self.round_number - 1] +
                 ' und 0 Punkte sonst'
                 # ', falls ' +
                 # Constants.ctext[self.round_number - 1]
                ]
                ,
                ['C',
                 str((10 - self.player.q_now) * 10) +
                 ' Punkte, falls ' +
                 Constants.ctext[self.round_number - 1] +
                 ' und 0 Punkte sonst'
                 # ', falls ' +
                 # Constants.etext[self.round_number - 1]
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
        return [loc_list[i] for i in [0]]



    title = extract(title_all)
    explaintext = extract(explaintext_all)
    ctext_short = extract(ctext_short_all)
    etext_short = extract(etext_short_all)
    mtext = extract(mtext_all)
    ctext = extract(ctext_all)
    etext = extract(etext_all)


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    eventTRUE = models.BooleanField()
    number_draw = models.IntegerField()
    title = models.StringField()

class Player(BasePlayer):

    # treatments
    treatment = models.IntegerField()
    prize = models.StringField()

    # payoff
    payoffq = models.IntegerField()
    x = models.FloatField()
    points = models.IntegerField()

    input = models.BooleanField(label="red?")
    draw = models.IntegerField(label="number drawn?")

    # safes number of red draws in update
    input_update = models.IntegerField(label="Number of red draws?")

    # ------ Money reward assignment
    def random_money_assignment(self):
        # randomize to treatments
        cur_random = random.choice(["2 Euro"])
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
    def compute_points(self):
        if self.x is None:
            self.x = 0
            print("self.x is None")
        if self.payoffq is None:
           self.payoffq = 0
           print("self.payoffq is None")
        return(round(100*(self.payoffq/10 * self.x * self.group.eventTRUE +
               (1-self.payoffq/10) * (1-self.x) * (1-self.group.eventTRUE))))
    def number_selected_bet(self):
        return(self.payoffq+1)

    def tickets_prize_text(self):
        return(self.prize)

