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

    name_in_url = 'urninfo'
    players_per_group = None
    num_rounds = 2

    # minutes in topic before time out
    minutes = 8

    # safes all types of elicitation in dynamic page
    elicit_types = ["choice_twice", "slider"]

    q_transform_types = [True, False]

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
        4,
        6,
        1,
        9,
        3,
        8,
        2,
        7,
    ]
    dynamic_question_number = 5

    # Title at the top of each page
    title_all = ["gepunkteter Ball nach 10 Ziehungen",
               ]

    # Text used to explain the domain at explanation page
    explaintext_all = [
       "Der Experimentleiter wird einen Ball aus der Urne ziehen. In der Urne sind 90 Bälle. Von 60 roten Bällen ist eine Ihnen unbekannte Anzahl gepunktet. Wir betrachten ob ein gepunkteter Ball gezogen wird oder ein einfarbiger. Im Vergleich zu vorher haben Sie zusätzliche Informationen über die Anzahl gepunkteter Bälle, da Sie bereits 10 Ziehungen gesehen haben.",
    ]
    # Short summary of event
    ctext_short_all = [
        "einfarbiger Ball",
    ]
    # Short summary of complement
    etext_short_all = [
        "gepunkteter Ball",
    ]
    # Text used to describe the event
    ctext_all = [
        "ein einfarbiger Ball gezogen wird",
    ]
    # Text used to describe the complement
    etext_all = [
        "ein gepunkteter Ball gezogen wird",
    ]

    # Text used to describe to desribe independence
    mtext_all = [
        "gezogenen Ball",
    ]

    text_choice = "10 Euro falls..."

    def make_field(label):
        return models.StringField(
            label=label,
            widget=widgets.RadioSelect,
            blank=True,
        )


    def extract(loc_list):
        return loc_list

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
    eventTRUE = models.BooleanField(label="True or not?")



class Player(BasePlayer):

    # treatments
    treatment = models.IntegerField()
    prize = models.StringField()
    title = models.StringField()
    q_transform = models.BooleanField(initial=True)

    # payoff
    x = models.FloatField()

    # ------ Dynamic page
    # safes input
    val_now = Constants.make_field(Constants.text_choice)
    val_now1 = Constants.make_field(Constants.text_choice)
    val_now2 = Constants.make_field(Constants.text_choice)
    val_now3 = Constants.make_field(Constants.text_choice)
    scoreE = models.IntegerField(blank=True)
    scoreC = models.IntegerField(blank=True)

    val_first = Constants.make_field(Constants.text_choice)
    val_second = Constants.make_field(Constants.text_choice)

    # safes if slider was moved
    checkslider = models.IntegerField(blank=True)
    # safes intern round in dynamic page
    dyn_round = models.IntegerField()
    # safes position for which mixing is irrational below
    mix_lower = models.FloatField(initial=0)
    # safes position for which mixing is irrational above
    mix_upper = models.FloatField(initial=10)
    # safes if dynamic already finished
    dynamic_end = models.BooleanField(initial=False)
    # safes current q
    q_intern = models.FloatField(initial=5) # safes untransformed
    q_now = models.FloatField(initial=5)
    qnot_now = models.FloatField(initial=5)
    qmix_now = models.FloatField(initial=5)
    # safes counter for which results are shown
    results_counter = models.IntegerField(initial=0)
    # safes question order
    choices_order = models.LongStringField(initial="O")
    # safes all input
    dyn_all = models.StringField(initial="S")

    # safes current elicitation type
    elicit_type = models.StringField()

    # safes slider dyn output
    val_slider_dyn = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")

    # counts how many of the qs where asked (vs skipped)
    num_questions_asked = models.IntegerField(initial=0)
    topic_number = models.IntegerField(initial=1)
    topic_number_total = models.IntegerField(initial=Constants.num_rounds/2)

    # returns right q in dynamic page
    def assign_q(self):

        print("Dyn_round is ", self.dyn_round, "and bounds are [", self.mix_lower,self.mix_upper,"]")

        if self.dyn_round < len(self.participant.vars['q']):
            loc_q = self.participant.vars['q'][self.dyn_round]
            if loc_q > self.mix_upper or loc_q < self.mix_lower:
                self.dyn_round = self.dyn_round + 1
                print("drawn q is ", loc_q, " and out of interval [", self.mix_lower, self.mix_upper, "]")
                self.assign_q()
                return
        else:
            print("Regular qs finished, start random draws")
            loc_q = random.sample(self.participant.vars['q_free'],1)[0]

        if self.q_transform:
            self.q_now = loc_q / max(loc_q, 10 - loc_q) * 10
            self.qnot_now = (10 - loc_q)/ max(loc_q, 10 - loc_q) * 10
            self.qmix_now = loc_q*(10-loc_q) / max(loc_q, 10 - loc_q) * 10
        else:
            self.q_now = loc_q
            self.qnot_now = 10 - loc_q
            self.qmix_now = loc_q*(10-loc_q)

        self.q_intern = loc_q
        self.dyn_round = self.dyn_round + 1
        self.num_questions_asked = self.num_questions_asked + 1
        print("UUUUU BEFORE:", self.participant.vars['q_free'])
        self.participant.vars['q_free'].remove(loc_q)
        print("UUUUU AFTER:", self.participant.vars['q_free'])

        if self.num_questions_asked > Constants.dynamic_question_number:
            print("dynamic end set to true")
            self.dynamic_end = True




    def get_winning_chance_dyn(self):
        loc_x = self.x
        loc_q = self.q_now
        loc_qnot = self.qnot_now
        return (round(100 * (
                loc_q * loc_x * self.group.eventTRUE +
                loc_qnot * (1 - loc_x) * (1 - self.group.eventTRUE))))

    topic = models.IntegerField(initial=0)

    # methods to put text in templates
    def fun_title(self):
        return (Constants.title[self.topic])

    def etext_short(self):
        return (Constants.etext_short[self.topic])

    def ctext_short(self):
        return (Constants.ctext_short[self.topic])

    def fun_etext(self):
        return (Constants.etext[self.topic])

    def fun_ctext(self):
        return (Constants.ctext[self.topic])

    def fun_mtext(self):
        return (Constants.mtext[self.topic])

    def fun_explanation(self):
        return (Constants.explaintext[self.topic])




    # makes text for choice page in dynamic context
    def make_text_dynamic(self):

        if round(self.qnot_now * 10) < 100:
            c_desc = Constants.ctext[self.topic] +\
                      " und Sie zusätzlich eine Zahl von 1 bis " +\
                      str(round(self.qnot_now * 10)) +\
                      ' ziehen.'
        else:
            c_desc =  Constants.ctext[self.topic] +\
                      "."

        if round(self.q_now * 10) < 100:
            e_desc =  Constants.etext[self.topic] +\
                     " und Sie zusätzlich eine Zahl von 1 bis " +\
                     str(round(self.q_now * 10)) +\
                     ' ziehen.'
        else:
            e_desc = Constants.etext[self.topic] +\
            "."

        m_desc = "Sie eine Zahl von 1 bis " +\
                 str(round(self.qmix_now)) +\
                 " ziehen."

        return [['M', m_desc]
                ,
                ['E',e_desc]
                ,
                ['C',c_desc]
                ]
