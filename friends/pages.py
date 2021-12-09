from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class friends(Page):
    pass


class Intro(Page):
    # safe which question relevant for payoff
    def before_next_page(self):
        self.participant.vars['payoff_title'] = Constants.payoff_topic
        self.participant.vars['payoff_number'] = Constants.payoff_num


class Intro2(Page):
    pass


class IntroWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class ReadyWaitPage(WaitPage):
    pass



page_sequence = [
    friends,
    Intro,
    IntroWaitPage,
    Intro2,
    ReadyWaitPage,
]
