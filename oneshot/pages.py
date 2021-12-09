from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random
import time


class explanation(Page):
    form_model = 'player'

    def vars_for_template(self):
        return {
                'round_number': self.round_number-1,
                'treatment': self.player.treatment,
                }

    def before_next_page(self):
        self.group.title = self.player.fun_title()
        self.player.dyn_round = 0
        print("Assign dyn_round: ", self.player.dyn_round)

        # choose elicitation type
        if self.round_number is 1:
            self.player.participant.vars['elicit_type'] = Constants.elicit_types[self.player.id_in_group % len(Constants.elicit_types)]
        self.player.elicit_type = self.player.participant.vars['elicit_type']

        # randomly choose order of questions
        self.player.participant.vars['q'] = random.sample(Constants.q, Constants.dynamic_question_number)
        print("the list of qs is", self.player.participant.vars['q'])

        # assign new q when initializing page
        self.player.q_now = self.player.get_q_now()
        print("Just assigned q_now:", self.player.q_now)

        # assign new money value
        self.player.random_money_assignment()

        # start time out time
        self.participant.vars['expiry'] = time.time() + Constants.minutes * 60


class dynamicPage(Page):
    form_model = 'player'
    form_fields = ['val_now', 'valtdyn', 'valtdynb', "val_slider_dyn"]

    def vars_for_template(self):
        return {
                'round_number': self.round_number-1,
                'dynamic_counter': self.player.dyn_round,
                'q_now': self.player.q_now * 10,
                'q_not_now': 100 - self.player.q_now * 10,
        }

    def val_now_choices(self):
        options = Constants.make_text_dynamic(self)
        random.shuffle(options)
        self.player.choices_order = self.player.choices_order + str(options)
        return options

    # error message tickets
    def error_message(self, values):
        print('values is', values)

        if values["valtdyn"] is None:
            values["valtdyn"] = 0

        if values["valtdynb"] is None:
            values["valtdynb"] = 0

        if self.player.elicit_type == "ticket":
            if (values["valtdyn"] + values["valtdynb"]) != 100:
                return 'Sie müssen insgesamt genau 100 Tickets setzen.'

    def is_displayed(self):

        # don't display if timeout
        if self.participant.vars['expiry'] - time.time() > 3:
            False

        # show page if not yet finished
        if self.player.id_in_group == 1:
            return False
        else:
            if self.player.dynamic_end is False:
                return True
            else:
                return False

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def before_next_page(self):

        if not self.timeout_happened:
            if self.player.elicit_type == "choice":
                response = getattr(self.player, 'val_now')
                self.player.x = \
                    0 if response == "C" \
                        else 1 if response == "E" \
                        else 1 - self.player.q_now / 10
                self.player.val_now = None


            if self.player.elicit_type == "ticket":
                self.player.x = self.player.valtdyn / 100
                self.player.valtdyn = None
                self.player.valtdynb = None

            if self.player.elicit_type == "slider":
                self.player.x = 1- self.player.val_slider_dyn / 100
                self.player.val_slider_dyn = None

            # adapt bounders upper and lower mixing
            if self.player.x == 0:
               print("new lower:", self.player.q_now)
               self.player.mix_lower = self.player.q_now
            if self.player.x == 1:
                print("new upper:", self.player.q_now)
                self.player.mix_upper = self.player.q_now

            # round choice
            self.player.x = round(self.player.x, ndigits=2)
            self.player.payoffq = self.player.q_now

            # safe full situation in String
            self.player.dyn_all = self.player.dyn_all + " | " + str(self.player.q_now) + "," + str(self.player.x)

            # assign new q_now
            self.player.q_now = self.player.get_q_now()
            print("Just assigned q_now:", self.player.q_now)

            # set starting value for next dynamic to NA
            self.player.val_now = None



class AllGroupsWaitPage(WaitPage):
    wait_for_all_groups = True



class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class input(Page):
    form_model = 'player'
    form_fields = ['input']

    def is_displayed(self):
        return self.player.id_in_group is 1

    def before_next_page(self):
        self.group.eventTRUE = self.player.input


class input_number(Page):
    form_model = 'player'
    form_fields = ['draw']

    def is_displayed(self):
        return self.player.id_in_group is 1

    def before_next_page(self):
        # safe drawn number
        self.group.number_draw = self.player.draw






class Results(Page):
    pass


class Results_absolute(Page):

    def before_next_page(self):
        # add to payoff
        if self.group.number_draw <= self.player.compute_points():
            print("Someone won 2 EUR")
            self.participant.payoff = self.participant.payoff + c(2)



page_sequence = [
    explanation,
    dynamicPage,
    input,
    AllGroupsWaitPage,
    Results,
    input_number,
    AllGroupsWaitPage,
    Results_absolute,
]
