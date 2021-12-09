from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstPage(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']

    def before_next_page(self):
        if self.player.id_in_group % 4 is 1:
            self.player.int1 = 175
            self.player.int2 = 200
            self.player.int3 = 225
        elif self.player.id_in_group % 4 is 2:
            self.player.int1 = 225
            self.player.int2 = 250
            self.player.int3 = 275
        elif self.player.id_in_group % 4 is 3:
            self.player.int1 = 150
            self.player.int2 = 200
            self.player.int3 = 250
        else:
            self.player.int1 = 200
            self.player.int2 = 250
            self.player.int3 = 300

class MyPage(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class IP(Page):
    form_model = 'player'

    form_fields = ["qsrcloudquestion1","qsrcloudquestion2","qsrcloudquestion3","qsrcloudquestion4"]

    def is_displayed(self):
        print(self.player.int1)
        return self.player.participant.vars['participant']

    def error_message(self, values):
        if values["qsrcloudquestion1"] + values["qsrcloudquestion2"] + values["qsrcloudquestion3"] + values['qsrcloudquestion4'] != 100:
            return "Die Antworten müssen zusammen 100% ergeben! Momentan ergeben Ihre Antworten zusammen {}%.".format(values["qsrcloudquestion1"]+values["qsrcloudquestion2"]+values["qsrcloudquestion3"]+ values['qsrcloudquestion4'])


class Results(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


page_sequence = [
    FirstPage,
    MyPage,
    IP,
    Results
]
