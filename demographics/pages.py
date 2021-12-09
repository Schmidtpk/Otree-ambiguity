from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['birthday', 'gender', 'fieldofstudy','profession','moneyathand','probabilityexp1','probabilityexp2', 'probabilityexp3', 'probabilityexp4', 'probabilityexp5', 'comprehension',]

    def is_displayed(self):
        return self.player.participant.vars['participant']

    def before_next_page(self):
        print(c(self.participant.payoff))
        print(c( self.participant.vars['epoints'] )*1000 if self.group.eventTRUE else c( self.participant.vars['cpoints'] )*1000)
        self.participant.payoff = c(self.participant.payoff) + c( self.participant.vars['epoints'] )*1000 if self.group.eventTRUE else c(self.participant.payoff) + c( self.participant.vars['cpoints'] )*1000
        print(c(self.participant.payoff))



class RiskAversion(Page):
    form_model = 'player'
    form_fields = ['riskaversion']

    def is_displayed(self):
        return self.player.participant.vars['participant']

    def riskaversion_choices(self):
        return [
            ["1", "8 Euro sicher"],
            ["2", "6 Euro falls Sie eine Zahl von 1 bis 50 ziehen und 12 Euro falls Sie eine Zahl von 51 bis 100 ziehen"],
            ["3", "4 Euro falls Sie eine Zahl von 1 bis 50 ziehen und 16 Euro falls Sie eine Zahl von 51 bis 100 ziehen"],
            ["4", "0 Euro falls Sie eine Zahl von 1 bis 50 ziehen und 24 Euro falls Sie eine Zahl von 51 bis 100 ziehen"],
        ]


class AmbAversion(Page):
    form_model = 'player'
    form_fields = ['amb_aversion']

    def amb_aversion_choices(self):
        return [
            ["1", "8 Euro sicher"],
            ["2", "6 Euro, falls ein roter Ball gezogen wird und 12 Euro, falls ein blauer Ball gezogen wird"],
            ["3", "4 Euro, falls ein roter Ball gezogen wird und 16 Euro, falls ein blauer Ball gezogen wird"],
            ["4", "0 Euro, falls ein roter Ball gezogen wird und 24 Euro, falls ein blauer Ball gezogen wird"],
        ]


class ThankYou(Page):

    def is_displayed(self):
        return self.player.participant.vars['participant']

    def vars_for_template(self):
        return {
            'true_event': self.participant.vars['e'] if self.group.eventTRUE else self.participant.vars['c'],
            'title': self.session.vars["payoff_title"] if 'payoff_title' in self.session.vars else 'NA',
            'money': self.player.participant.vars['money'] if 'money' in self.participant.vars else 'NA',
            'points_lot': round(self.player.participant.vars['epoints']) if self.group.eventTRUE else round(self.player.participant.vars['cpoints']),
            'epoints': round(self.player.participant.vars['epoints']) if 'epoints' in self.participant.vars else 'NA',
            'e': self.player.participant.vars['e'] if 'e' in self.participant.vars else 'NA',
            'cpoints': round(self.player.participant.vars['cpoints']) if 'cpoints' in self.participant.vars else 'NA',
            'c': self.player.participant.vars['c'] if 'c' in self.participant.vars else 'NA',
        }





class Input(Page):
    form_model = 'group'
    form_fields = ['eventTRUE']

    def is_displayed(self):
        return self.player.participant.vars['participant'] is False


class Getmoney(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']





page_sequence = [
    # ResultsWaitPage,
    # AmbAversion,
    # ResultsWaitPage,
    # RiskAversion,
    Demographics,
    Input,
    ThankYou,
    # Draw,
    # DrawWait,
    # ThankYou2,
    # Getmoney,
]
