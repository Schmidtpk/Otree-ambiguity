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

    prize = "10 Euro"

    a = [
        # 1,
        2,
        # 3,
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
    dynamic_question_number = 4

    # Title at the top of each page
    title_all = ["blauer Ball aus Urne",
                 "gepunkteter Ball aus Urne",
                 # "Ball aus ?-Urne",
                 # "Ball aus 5/5-Urne",
                 "DAX",]

    # Text used to explain the domain at explanation page
    explaintext_all = [
        "Der Experimentleiter wird einen Ball aus der Urne ziehen. In der Urne sind 30 Bälle. 10 Bälle sind blau. Die anderen 20 Bälle sind rot. Wir betrachten ob ein blauer Ball gezogen wird oder ein roter.",
        "Der Experimentleiter wird einen Ball aus der Urne ziehen. In der Urne sind 30 Bälle. Von 20 roten Bällen ist eine Ihnen unbekannte Anzahl gepunktet. Wir betrachten ob ein gepunkteter Ball gezogen wird oder ein einfarbiger.",
        # "Der Experimentleiter wird einen Ball aus der ?-Urne ziehen. In der Urne sind 10 Bälle, die blau oder rot sind. Die Anzahl an blauen und roten Bällen in der Urne ist unbekannt.",
        # "Der Experimentleiter wird einen Ball aus der 5/5-Urne ziehen. In der Urne sind 5 blaue und 5 rote Bälle.",
        "Der DAX-Kurs zum Einstieg des Experiments steht an der Tafel. Am Ende des Experiments wird der DAX-Kurs erneut abgefragt. Wir werden betrachten, ob der DAX über den an der Tafel gennanten Betrag gestiegen ist oder nicht.",
    ]
    # Short summary of event
    ctext_short_all = [
        "roter Ball",
        "einfarbiger Ball",
        # "blauer Ball",
        # "blauer Ball",
        "DAX fällt",
    ]
    # Short summary of complement
    etext_short_all = [
        "blauer Ball",
        "gepunkteter Ball",
        # "roter Ball",
        # "roter Ball",
        "DAX steigt",
    ]
    # Text used to describe the event
    ctext_all = [
        "ein roter Ball gezogen wird",
        "ein einfarbiger Ball gezogen wird",
        # "ein blauer Ball gezogen wird",
        # "ein blauer Ball gezogen wird",
        "der DAX fällt",
    ]
    # Text used to describe the complement
    etext_all = [
        "ein blauer Ball gezogen wird",
        "ein gepunkteter Ball gezogen wird",
        # "ein roter Ball gezogen wird",
        # "ein roter Ball gezogen wird",
        "der DAX steigt",
    ]

    # Text used to describe to desribe independence
    mtext_all = [
        "gezogenen Ball",
        "gezogenen Ball",
        # "gezogenen Ball",
        # "gezogenen Ball",
        "DAX",
    ]

    text_choice = "10 Euro falls..."

    def make_field(label):
        return models.StringField(
            label=label,
            widget=widgets.RadioSelect,
            blank=True,
        )


    def extract(loc_list):
        return [loc_list[i] for i in [0, 1, 2]]

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
    num_participants = models.IntegerField(label="how many?", initial=1)


class Player(BasePlayer):
    val_slider_dyn = models.IntegerField(widget=widgets.Slider(attrs={'step': '10'}, show_value=False),
                                         blank=True,
                                         label="")
    # safes if slider was moved
    checkslider = models.IntegerField(blank=True)

    elicit_type = models.StringField(initial="slider")

    topic = models.IntegerField(initial=0)

    test_questions1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)

    test_simple1 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)

    test_simple2 = models.StringField(label="Welche Aussage ist richtig?",
                                       widget=widgets.RadioSelect)

    test_event1 = models.StringField(label="Welche Aussage lässt sich sicher aus obiger Beschreibung ableiten?",
                                       widget=widgets.RadioSelect)

    test_event2 = models.StringField(label="Sie wissen sicher, dass...",
                                       widget=widgets.RadioSelect)

    test_event3 = models.StringField(label="Welche Aussage ist richtig?",
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
