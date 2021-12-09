from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random

class GroupPage(WaitPage):
    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):
        if len(waiting_players) == self.session.vars["num_participants"]:
            print("All players present")
            return waiting_players
        else:
            print(len(waiting_players), " of ", self.session.vars["num_participants"], "players waiting")


class Dropout(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class ExplanationQuestions(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class TestQuestions(Page):
    form_model = 'player'
    form_fields = ['test_questions1',
                   'test_questions2']

    def test_questions1_choices(self):
        return [["F", "Sie können 10 Euro gewinnen."],
                ["T", "Sie können 20 Euro gewinnen."],
                ]


    def test_questions2_choices(self):
        return [["F", "Die Ergebnisse der ersten Frage sind relevant für Ihre Auszahlung."],
                ["T", "Die Ergebnisse der zweiten Frage sind relevant für Ihre Auszahlung."],
                ["F", "Die Ergebnisse der dritten Frage sind relevant für Ihre Auszahlung."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']


class ResultQuestions(Page):
    def before_next_page(self):
        if self.player.test_questions1 == "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_questions2 == "F":
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']


class ExplanationPoints(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class TestPoints(Page):
    form_model = 'player'
    form_fields = ['test_points1',
                   'test_points2']

    def test_points1_choices(self):
        return [["F", "Sie gewinnen 10 Euro."],
                ["F", "Sie gewinnen 20 Euro."],
                ["T", "Sie gewinnen 0 Euro."],
                ]

    def test_points2_choices(self):
        return [["F", "Wenn Sie statt der Zahl 61 die Zahl 40 gezogen hätten, würden Sie Geld gewinnen"],
                ["T", "Wenn Sie statt 35 Punkte in der ausgewählten Frage 70 Punkte erspielt hätten, würden Sie Geld gewinnen"],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultPoints(Page):
    def before_next_page(self):
        if self.player.test_points1 == "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_points2 == "F":
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ExplanationSlider(Page):
    form_model = 'player'
    form_fields = ['example_slider']

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider(Page):
    def before_next_page(self):
        if self.player.example_slider is not 80:
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestSlider1(Page):
    form_model = 'player'
    form_fields = ['example_slider1']

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider1(Page):
    def before_next_page(self):
        if self.player.example_slider1 is not None:
            if self.player.example_slider1 > 0:
                self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestSlider2(Page):
    form_model = 'player'
    form_fields = ['example_slider2']

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider2(Page):
    def before_next_page(self):
        if self.player.example_slider2 is not None:
            if self.player.example_slider2 < 100:
                self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestSlider3(Page):
    form_model = 'player'
    form_fields = ['example_slider3']

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider3(Page):
    def before_next_page(self):
        if self.player.example_slider3 is not 70:
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestAll1(Page):
    form_model = 'player'
    form_fields = ['test_all1', "test_all2"]

    def test_all1_choices(self):
        return [["F", "Sie gewinnen in dieser Situation 20 Euro."],
                ["F", "Sie gewinnen in dieser Situation 10 Euro."],
                ["T", "Sie gewinnen in dieser Situation nichts."],
                ]

    def test_all2_choices(self):
        return [["T", "Alles andere unverändert, gewinnen Sie 20 Euro, falls der DAX steigt."],
                ["F", "Alles andere unverändert, gewinnen Sie nichts, falls der DAX steigt."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultAll1(Page):
    def before_next_page(self):
        if self.player.test_all1 is "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_all2 is "F":
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestAll2(Page):
    form_model = 'player'
    form_fields = ['test_all3', "test_all4"]

    def test_all3_choices(self):
        return [["F", "Sie gewinnen in dieser Situation 20 Euro."],
                ["T", "Sie gewinnen in dieser Situation 10 Euro."],
                ["F", "Sie gewinnen in dieser Situation nichts."],
                ]

    def test_all4_choices(self):
        return [["T", "Alles andere unverändert, gewinnen Sie 10 Euro, falls der DAX steigt."],
                ["F", "Alles andere unverändert, gewinnen Sie 10 Euro, falls Sie am Ende eine 80 ziehen."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultAll2(Page):
    def before_next_page(self):
        if self.player.test_all3 is "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_all4 is "F":
            self.player.mistakes = self.player.mistakes + 1


class ExplanationWaitPage(WaitPage):
    template_name = 'tests/MyWaitPage.html'


class ExplanationReady(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class TotalResults(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']



page_sequence = [

    GroupPage,
    Dropout,

    ExplanationQuestions,
    TestQuestions,
    ResultQuestions,

    ExplanationPoints,
    TestPoints,
    ResultPoints,

    ExplanationSlider,
    ResultSlider,
    TestSlider1,
    ResultSlider1,
    TestSlider2,
    ResultSlider2,
    TestSlider3,
    ResultSlider3,

    TestAll1,
    ResultAll1,
    TestAll2,
    ResultAll2,

    ExplanationWaitPage,

    TotalResults,
]
