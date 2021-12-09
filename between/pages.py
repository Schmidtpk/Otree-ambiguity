from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Intro(Page):
    pass


class Intro2(Page):
    pass


class IntroWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class ReadyWaitPage(WaitPage):
    pass



page_sequence = [
    IntroWaitPage,
    Intro,
    Intro2,
    ReadyWaitPage,
]