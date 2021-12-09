from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class GroupPage(WaitPage):
    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):
        if len(waiting_players) == self.session.vars["num_participants"]:
            print("All players present")
            return waiting_players
        else:
            print(len(waiting_players), " of ", self.session.vars["num_participants"], "players waiting")

class Explanation(Page):
    pass

class RiskQuestion(Page):
    form_model = 'player'
    form_fields = [
        'risk_choice'
    ]

    def risk_choice_choices(self):
        return [["safe", "Sie erhalten 2 Euro."],
                ["risky", "Sie erhalten 5 Euro falls Sie eine Zahl von 1 bis 50 ziehen und nichts falls Sie eine Zahl von 51 bis 100 ziehen."],
                ["risky2", "Sie erhalten 10 Euro falls Sie eine Zahl von 1 bis 30 ziehen und nichts falls Sie eine Zahl von 31 bis 100 ziehen."],
        ]

    def before_next_page(self):

        if self.player.risk_choice == "risky":
            self.player.participant.vars["risk"] = "Sie bekommen 5 Euro, falls Sie eine Zahl von 1 bis 50 ziehen. Bitte warten Sie bis Sie an der Reihe sind."
        elif self.player.risk_choice == "safe":
            self.player.participant.vars["risk"] = "Sie bekommen 2 Euro. Bitte warten Sie bis die anderen Teilnehmer eine Zahl gezogen haben."
        else:
            self.player.participant.vars["risk"] = "Sie bekommen 10 Euro, falls Sie eine Zahl von 1 bis 30 ziehen. Bitte warten Sie bis Sie an der Reihe sind."

class RiskResult(Page):
    pass

page_sequence = [
    GroupPage,
    Explanation,
    RiskQuestion,
]
