from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to Kooperieren or Alleingang. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'prisoner/instructions.html'

    # payoff if 1 player Alleingangs and the other Kooperierens""",
    betray_payoff = 3
    betrayed_payoff = 0

    # payoff if both players Kooperieren or both Alleingang
    both_cooperate_payoff = 2
    both_defect_payoff = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    payoff_cur = models.IntegerField()

    decision = models.StringField(
        choices=['Cooperate', 'Defect'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = dict(
            Cooperate=dict(
                Cooperate=Constants.both_cooperate_payoff,
                Defect=Constants.betrayed_payoff
            ),
            Defect=dict(
                Cooperate=Constants.betray_payoff,
                Defect=Constants.both_defect_payoff
            )
        )

        if self.decision is '' or self.other_player().decision is '':
            self.payoff_cur = 0
        else:
            self.payoff_cur = payoff_matrix[self.decision][self.other_player().decision]
