from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Asking for demographic information and some additional questions
"""

class Constants(BaseConstants):
    name_in_url = 'demographics'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    eventTRUE = models.BooleanField()

class Player(BasePlayer):
    draw = models.IntegerField(label="Number drawn?")


    # RISK and Ambiguity AVERSION
    amb_aversion = models.StringField(
            label="Was bevorzugen Sie?",
            widget=widgets.RadioSelect)
    riskaversion = models.StringField(
            label="Was bevorzugen Sie?",
            widget=widgets.RadioSelect)

    # Demographics
    birthday = models.StringField(verbose_name='Bitte geben Sie ihr Geburtsjahr an:')

    gender = models.StringField(initial=None,
                                choices=['weiblich', 'männlich'],
                                verbose_name='Was ist ihr Geschlecht?',
                                widget=widgets.RadioSelect())

    profession = models.StringField(initial = None,
                                  verbose_name='Was ist ihr Beruf?')

    fieldofstudy = models.StringField(blank=True,
                                    initial = None,
                                    choices= ['Rechtswissenschaft', 'Wirtschaftswissenschaften', 'Gesellschaftswissenschaften', 'Erziehungswissenschaften', 'Psychologie', 'Sportwissenschaften', 'Theologie', 'Sprach-und Kulturwissenschaften', 'Geowissenschaften', 'Informatik', 'Mathematik' , 'Physik', 'Biochemie, Chemie, Pharmazie', 'Medizin', 'Andere'],
                                    verbose_name='In welchem Bereich studieren Sie?',
                                    widget=widgets.Select())

    moneyathand = models.StringField(initial = None,
                                   choices = ['weniger als 250', '251 - 500', '501 - 750', '751 - 1000', 'mehr als 1000'],
                                   verbose_name='Wieviel Geld haben Sie monatlich (inkl. Miete) ca. zur Verfügung (in Euro)?',
                                   widget = widgets.Select())

    probabilityexp1 = models.PositiveIntegerField(initial = None,
                                        choices = range(1,8),
                                        verbose_name='Auf einer Skala von 1 (sehr wenig) - 7 (sehr viel), wieviel Erfahrung haben Sie mit Wahrscheinlichkeitsrechnung und Statistik?',
                                        widget= widgets.RadioSelect())

    probabilityexp2 = models.PositiveIntegerField(initial=None,
                                              choices=range(1, 8),
                                              verbose_name='Auf einer Skala von 1 (sehr wenig) - 7 (sehr viel), wieviel'
                                                           ' Erfahrung haben Sie mit Glücksspielen?',
                                              widget=widgets.RadioSelect())

    probabilityexp3 = models.StringField(initial=None,
                                    choices=['Ja', 'Nein'],
                                    verbose_name='Haben Sie je einen Universitätskurs zu Statistik oder Wahrscheinlichkeitstheorie besucht?',
                                    widget=widgets.RadioSelect())

    probabilityexp4 = models.FloatField(initial=None, verbose_name="Wie oft würfelt man im Durchschnitt eine gerade Zahl, wenn man einen normalen sechs-seitigen Würfel 1000 Mal würfelt?")

    probabilityexp5 = models.FloatField(initial=None, verbose_name="Nehmen Sie an, sie würden zweimal von den Zahlen von 1 bis 100 eine Zufallszahl ziehen. Sie gewinnen 10 Euro, falls beide Zahlen kleiner als 51 sind. Was würden Sie sagen ist die Chance in Prozent, dass Sie 10 Euro gewinnen?",
                                        min = 0, max = 100)

    comprehension = models.StringField(initial=None,
                                    choices=['Ja', 'Nein'],
                                    verbose_name='Glauben Sie, dass Sie den Auszahlungsmechanismus für die Schätzfragen vollständig verstanden haben?',
                                    widget=widgets.RadioSelect())


