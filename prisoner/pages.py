from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants



class Introduction(Page):
    timeout_seconds = 180
    def is_displayed(self):
        return self.player.participant.vars['participant']


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']



class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision
        )


    def before_next_page(self):
        me = self.player
        opponent = me.other_player()
        self.player.participant.vars['my_decision'] = me.decision
        self.player.participant.vars['he_decision'] = opponent.decision
        self.player.participant.vars['dilemma_payoff'] = self.player.payoff_cur
        self.participant.payoff = self.participant.payoff + c(self.player.payoff_cur)


page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results
]
