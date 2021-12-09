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
    name_in_url = 'ambiguity'
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
        4,
        6,
        1,
        9,
        3,
        8,
        2,
        7,
    ]
    dynamic_question_number = 9

    # Title at the top of each page
    title_all = ["Münze",
             "Ball aus Urne",
             "Würfel eine 6",
             "Münze und Urne",
             "Unbekanntes aus Urne",
             "Höchstemperatur Frankfurt 2018",
             "Höchstemperatur Tokio 2018",]

    # Text used to explain the domain at explanation page
    explaintext_all = [
        "Ein Teilnehmer wird eine Münze werfen. Die Münze hat eine Seite mit Kopf und eine Seite mit Zahl.",
        "Ein Teilnehmer hat 10 Bälle in eine Urne gelegt. Die Bälle sind blau und rot. Die Anzahl an blauen und roten Bällen in der Urne konnte der Teilnehmer frei wählen und ist geheim. Nun wird der Teilnehmer blind einen Ball aus der Urne ziehen.",
        "Ein Teilnehmer wird einen normalen sechseitigen Würfel werfen. Wir betrachten ob der Würfel eine 6 zeigt oder nicht.",
        "Ein Teilnehmer wird eine Münze werfen und 10 Bälle in eine Urne legen. Die Bälle sind blau und rot. Die Anzahl an blauen und roten Bällen in der Urne darf der Teilnehmer frei wählen und bleibt geheim. Anschließend wird ein Ball aus der Urne gezogen.",
        "Ein Teilnehmer wird diverse Gegenstände in eine Urne legen. Anschließend wird ein Gegenstand aus der Urne gezogen.",
        "Wir betrachten ob die höchste gemessene Temperatur in Frankfurt im Jahr 2018 höher oder niedriger als 37 ° C war.",
        "Wir betrachten ob die höchste gemessene Temperatur in Tokio (Japan) im Jahr 2018 höher oder niedriger als 37 ° C war.",
    ]
    # Short summary of event
    ctext_short_all = [
            "Kopf",
            "blauer Ball",
            "6",
            "Kopf und roter Ball",
            "kein Elefant",
            "niedriger als 37°C",
            "niedriger als 37°C",
    ]
    # Short summary of complement
    etext_short_all = [
        "Zahl",
        "roter Ball",
        "2, 3, 4, 5 oder 6",
        "Zahl oder blauer Ball",
        "ein Elefant",
        "höher als 37°C",
        "höher als 37°C",
        ]
    # Text used to describe the event
    ctext_all = [
            "die Münze Kopf zeigt",
            "ein blauer Ball gezogen wird",
            "der Würfel eine 6 zeigt",
            "die Münze Kopf zeigt und ein roter Ball gezogen wird",
            "kein Spielzeug Elefant gezogen wird",
            "die Höchstemperatur in Frankfurt unter 37 °C war",
            "die Höchstemperatur in Tokio (Japan) unter 37 °C war",
    ]
    # Text used to describe the complement
    etext_all = [
        "die Münze Zahl zeigt",
        "ein roter Ball gezogen wird",
        "der Würfel eine 1, 2, 3, 4 oder 5 zeigt",
        "die Münze Zahl zeigt oder ein blauer Ball gezogen wird",
        "ein Spielzeug Elefant gezogen wird",
        "die Höchstemperatur in Frankfurt über 37 °C war",
        "die Höchstemperatur in Tokio (Japan) über 37 °C war",
    ]
    # Text used to describe to desribe independence
    mtext_all = [
        "was die Münze zeigt",
        "was für ein Ball gezogen wird",
        "was der Würfel zeigt",
        "wie die Münze fällt und was aus der Urne gezogen wird",
        "was aus der Urne gezogen wird",
        "was die Höchstemperatur war",
        "was die Höchstemperatur war",
    ]
    results_all =[
        "Die Münze zeigt Kopf",
        "Ein roter Ball wurde gezogen",
        "Der Würfel zeigt 4",
        "Ein blauer Ball wurde gezogen und die Münze zeigt Zahl",
        "Es wurde kein Elefant gezogen.",
        "Der Höchstwert in Frankfurt war höher als 37 °C",
        "Der Höchstwert in Tokio war höher als 37 °C",
        ]
    eventTRUE_all = [
        0,
        0,
        1,
        1,
        0,
        1,
        1
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

    def make_text(q,self):
        return [['E',
                 str(Constants.a[q] * 10) +
                 ' Punkte, falls ' +
                 Constants.etext[self.round_number - 1] +
                ' (und keine Punkte sonst)'
                ]
                ,
                ['C',
                 str((10 - Constants.a[q]) * 10) +
                 ' Punkte, falls ' +
                 Constants.ctext[self.round_number - 1] +
                 ' (und keine Punkte sonst)'
                ]
                ,
                ['M',
                 str(Constants.a[q] * (10 - Constants.a[q])) +
                 " Punkte, egal " +
                 Constants.mtext[self.round_number-1]
                 ]
                ]

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
        return [loc_list[i] for i in [0, 1, 5, 6]]



    title = extract(title_all)
    eventTRUE = extract(eventTRUE_all)
    explaintext = extract(explaintext_all)
    ctext_short = extract(ctext_short_all)
    etext_short = extract(etext_short_all)
    mtext = extract(mtext_all)
    ctext = extract(ctext_all)
    etext = extract(etext_all)
    results = extract(results_all)


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        treatments = itertools.cycle([1, 2, 3])
        for p in self.get_players():
            p.treatment = next(treatments)


class Group(BaseGroup):
    eventTRUE = models.BooleanField()
    title = models.StringField()


class Player(BasePlayer):

    # treatments
    treatment = models.IntegerField()
    prize = models.CurrencyField()

    # payoff
    x = models.FloatField()

    input = models.BooleanField(label="True or not?")

    # ------ Money reward assignment
    def random_money_assignment(self):
        # randomize to treatments
        cur_random = random.choice([5, 5, 10])
        print("Random treatment assignment of ", cur_random)
        self.prize = c(cur_random)


    # ------ Dynamic page
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
                                         blank=True,
                                         label="")
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

    def get_winning_chance_dyn(self):
        loc_x = self.x
        loc_q = self.q_now
        return(round(100*(
                 loc_q * loc_x * self.group.eventTRUE +
                 (1-loc_q) * (1-loc_x) * (1-self.group.eventTRUE))))

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

    # text for ticketsPage
    def tickets_prize_text(self):
        return(str(self.prize))

