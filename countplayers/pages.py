from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants





class FirstPage(Page):
    def is_displayed(self):
        return self.player.id_in_group is not 1

    def before_next_page(self):
        self.participant.vars['payoff_title'] = "DAX"
        self.participant.vars['payoff_number'] = 2

        self.player.participant.vars['participant'] = True



class MyPage(Page):
    form_model = 'group'
    form_fields = ['num_participants']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def before_next_page(self):
        self.session.config['players_per_group'] = self.group.num_participants
        self.session.vars["num_participants"] = self.group.num_participants

        self.session.vars['payoff_title'] = 'DAX'
        self.session.vars['payoff_number'] = 2

        self.player.participant.vars['participant'] = False



class ReadyPage(Page):
    def is_displayed(self):
        return self.player.id_in_group is not 1



page_sequence = [
    FirstPage,
    MyPage,
    ReadyPage
]
