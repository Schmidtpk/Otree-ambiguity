from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random

class GroupPage(WaitPage):
    group_by_arrival_time = True
    template_name = 'tests/MyWaitPage.html'

    def vars_for_template(self):
        return {
            'body_text': self.player.participant.vars["risk"]
        }

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
    form_fields = ['test_questions1']

    def test_questions1_choices(self):
        return [["F", "Sie gewinnen 10 Euro."],
                ["T", "Sie gewinnen nichts."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']


class ResultQuestions(Page):
    def before_next_page(self):
        if self.player.test_questions1 == "F":
            self.player.mistakes = self.player.mistakes + 1


    def is_displayed(self):
        return self.player.participant.vars['participant']


class ExplanationPoints(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']

class ExplanationEvents(Page):
    form_model = 'player'
    form_fields = ['test_event1',
                   'test_event2',
                   'test_event3']

    def test_event1_choices(self):
        return [["T", "Jeder dritte Ball in der Urne ist blau"],
                ["F", "Jeder dritte Ball in der Urne ist gepunktet."],
                ]

    def test_event2_choices(self):
        return [["F", "... mehr gepunktete als einfarbige Bälle in der Urne sind."],
                ["T", "... mehr rote als blaue Bälle in der Urne sind."],
                ]

    def test_event3_choices(self):
        return [["T", "Es sind doppelt so viele rote Bäll wie blaue Bälle in der Urne."],
                ["F", "Es sind doppelt so viele gepunktete Bälle wie einfarbie Bälle in der Urne."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']

    def before_next_page(self):
        if self.player.test_event1 is "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_event2 is "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_event3 is "F":
            self.player.mistakes = self.player.mistakes + 1


class ResultEvents(Page):
    def is_displayed(self):
        return self.player.participant.vars['participant']


class ExplanationSimple(Page):
    form_model = 'player'
    form_fields = ['test_simple1',
                   'test_simple2']

    def test_simple1_choices(self):
        return [["F", "Sie gewinnen 10 Euro."],
                ["T", "Sie gewinnen nichts."],
                ]

    def test_simple2_choices(self):
        return [["T", "Alles sonst unverändert hätten Sie 10 Euro gewonnen, wenn Sie statt der Zahl 51 die Zahl 40 gezogen hätten"],
                ["F", "Alles sonst unverändert hätten Sie 10 gewonnen, wenn ein blauer Ball gezogen worden wäre."],
                ]

    def is_displayed(self):
        return self.player.participant.vars['participant']


class ResultSimple(Page):
    def before_next_page(self):
        if self.player.test_simple1 == "F":
            self.player.mistakes = self.player.mistakes + 1
        if self.player.test_simple2 == "F":
            self.player.mistakes = self.player.mistakes + 1

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
    form_fields = ['example_slider',
                   "val_slider_dyn",
                   'checkslider',]

    def vars_for_template(self):
        return {
                'round_number': 0,
                'dynamic_counter': 1,
                'q_now': 67,
                'q_not_now': 100,
                'prize_string': Constants.prize,
                'prize': c(10),
                'quote_e': 67,
                'quote_c': 100,
                'E_text': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'E_text_strong': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'C_text': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'C_text_strong': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'M_text': "So ist Ihre Auszahlung <b> unabhängig vom " + self.player.fun_mtext()+"</b>.",
                'image_path': '{}.jpeg'.format(self.player.fun_title()),
                'image_pathE': '{}.jpeg'.format("E_" + self.player.fun_title()),
                'image_pathC': '{}.jpeg'.format("C_" + self.player.fun_title()),
        }


    def checkslider_error_message(self, value):
            if not value and self.player.elicit_type == "slider":
                return 'Bitte bewegen Sie den Slider um eine Auswahl zu treffen.'


    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider(Page):
    def before_next_page(self):
        if self.player.val_slider_dyn is not 100:
            print("Mistake")
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestSlider1(Page):
    form_model = 'player'
    form_fields = ['example_slider',
                   "val_slider_dyn",
                   'checkslider',]

    def vars_for_template(self):
        return {
                'round_number': 0,
                'dynamic_counter': 1,
                'q_now': 100,
                'q_not_now': 11,
                'prize_string': Constants.prize,
                'quote_e': 100,
                'quote_c': 11,
                'E_text': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'E_text_strong': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'C_text': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'C_text_strong': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'M_text': "So ist Ihre Auszahlung <b> unabhängig vom " + self.player.fun_mtext()+"</b>.",
                'image_path': '{}.jpeg'.format(self.player.fun_title()),
                'image_pathE': '{}.jpeg'.format("E_" + self.player.fun_title()),
                'image_pathC': '{}.jpeg'.format("C_" + self.player.fun_title()),
        }

    def checkslider_error_message(self, value):
            if not value and self.player.elicit_type == "slider":
                return 'Bitte bewegen Sie den Slider um eine Auswahl zu treffen.'



class ResultSlider1(Page):
    def before_next_page(self):

        if self.player.val_slider_dyn is not 0:
            print("Mistake")
            self.player.mistakes = self.player.mistakes + 1
        self.player.topic = 1

    def is_displayed(self):
        return self.player.participant.vars['participant']

class TestSlider2(Page):
    form_model = 'player'
    form_fields = ['example_slider',
                   "val_slider_dyn",
                   'checkslider',]

    def vars_for_template(self):
        return {
                'round_number': 1,
                'dynamic_counter': 1,
                'q_now': 100,
                'q_not_now': 100,
                'prize_string': Constants.prize,
                'quote_e': 100,
                'quote_c': 100,
                'E_text': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'E_text_strong': "So setzen Sie auf <b>" + self.player.etext_short()+"</b> .",
                'C_text': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'C_text_strong': "So setzen Sie auf <b>" + self.player.ctext_short()+"</b> .",
                'M_text': "So ist Ihre Auszahlung <b> unabhängig vom " + self.player.fun_mtext()+"</b>.",
                'image_path': '{}.jpeg'.format(self.player.fun_title()),
                'image_pathE': '{}.jpeg'.format("E_" + self.player.fun_title()),
                'image_pathC': '{}.jpeg'.format("C_" + self.player.fun_title()),
        }

    def checkslider_error_message(self, value):
            if not value and self.player.elicit_type == "slider":
                return 'Bitte bewegen Sie den Slider um eine Auswahl zu treffen.'

    def is_displayed(self):
        return self.player.participant.vars['participant']

class ResultSlider2(Page):
    def before_next_page(self):
        if self.player.val_slider_dyn is not 50:
            self.player.mistakes = self.player.mistakes + 1

    def is_displayed(self):
        return self.player.participant.vars['participant']


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

    ExplanationEvents,
    ResultEvents,

    ExplanationSimple,
    ResultSimple,

    ExplanationSlider,
    ResultSlider,
    TestSlider1,
    ResultSlider1,
    TestSlider2,
    ResultSlider2,

    ExplanationWaitPage,

    TotalResults,
]
