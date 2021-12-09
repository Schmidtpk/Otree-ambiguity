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
        self.group.eventTRUE = Constants.eventTRUE[self.group.round_number-1]
        self.group.title = self.player.fun_title()
        self.player.dyn_round = 0
        print("Assign dyn_round: ", self.player.dyn_round)

        # choose elicitation type
        self.player.elicit_type = Constants.elicit_types[ (self.player.id_in_group-1) % len(Constants.elicit_types)]

        # randomly choose order of questions
        self.player.participant.vars['q'] = random.sample(Constants.a, Constants.dynamic_question_number)
        print("the list of qs is", self.player.participant.vars['q'])

        # assign new q when initializing page
        self.player.q_now = self.player.get_q_now()
        print("Just assigned q_now:", self.player.q_now)

        # assign new money value
        self.player.random_money_assignment()

        # start time out time
        self.participant.vars['expiry'] = time.time() + Constants.minutes * 60


class sliderPage(Page):
    form_model = 'player'
    form_fields = ['val_slider0', 'val_slider1', 'val_slider2', 'val_slider3', 'val_slider4',
                   'val_slider5', 'val_slider6', 'val_slider7', 'val_slider8']

    def vars_for_template(self):
        return {'rate_slider0': Constants.a[0], 'nrate_slider0': 10-Constants.a[0],
                'rate_slider1': Constants.a[1], 'nrate_slider1': 10-Constants.a[1],
                'rate_slider2': Constants.a[2], 'nrate_slider2': 10-Constants.a[2],
                'rate_slider3': Constants.a[3], 'nrate_slider3': 10-Constants.a[3],
                'rate_slider4': Constants.a[4], 'nrate_slider4': 10-Constants.a[4],
                'rate_slider5': Constants.a[5], 'nrate_slider5': 10-Constants.a[5],
                'rate_slider6': Constants.a[6], 'nrate_slider6': 10-Constants.a[6],
                'rate_slider7': Constants.a[7], 'nrate_slider7': 10-Constants.a[7],
                'rate_slider8': Constants.a[8], 'nrate_slider8': 10-Constants.a[8],
                'round_number': self.round_number-1,
                }

    def is_displayed(self):
        if self.player.id_in_group == 1:
            return False
        else:
            return (self.player.treatment + self.round_number) % 3 == 0

    def before_next_page(self):
        self.player.payoffq = random.choice(range(0, 8))
        self.player.x = 1 - getattr(self.player, 'val_slider{}'.format(self.player.payoffq)) / 100


class choicePage(Page):
    form_model = 'player'
    form_fields = ['val0', 'val1', 'val2', 'val3', 'val4',
                   'val5', 'val6', 'val7', 'val8']
    def vars_for_template(self):
        return {
                'cur_round': self.round_number-1
                }
    def val0_choices(self):
        return (Constants.make_text(0, self))
    def val1_choices(self):
        return(Constants.make_text(1,self))
    def val2_choices(self):
        return(Constants.make_text(2,self))
    def val3_choices(self):
        return(Constants.make_text(3,self))
    def val4_choices(self):
        return(Constants.make_text(4,self))
    def val5_choices(self):
        return(Constants.make_text(5,self))
    def val6_choices(self):
        return(Constants.make_text(6,self))
    def val7_choices(self):
        return(Constants.make_text(7,self))
    def val8_choices(self):
        return(Constants.make_text(8,self))

    def name_choice(self):
        return(self.player.x)

    def is_displayed(self):
        if self.player.id_in_group == 1:
            return False
        else:
            return (self.player.treatment + self.round_number) % 3 == 1

    def before_next_page(self):
        self.player.payoffq = random.choice(range(0, 8))
        response = getattr(self.player, 'val{}'.format(self.player.payoffq))
        self.player.x = \
            0 if response == "C" \
            else 1 if response == "E" \
            else 1 - Constants.a[self.player.payoffq]/10



class dynamicPage(Page):
    form_model = 'player'
    form_fields = ['val_now', 'valtdyn', 'valtdynb', "val_slider_dyn", "moved_slider"]

    def vars_for_template(self):
        return {
                'round_number': self.round_number-1,
                'dynamic_counter': self.player.dyn_round,
                'q_now': self.player.q_now * 10,
                'q_not_now': 100 - self.player.q_now * 10,
                'quote_e': self.player.q_now,
                'quote_c': 10 - self.player.q_now,
        }

    def val_now_choices(self):
        options = Constants.make_text_dynamic(self)
        random.shuffle(options)
        self.player.choices_order = self.player.choices_order + str(options)
        return options

    # error messages
    def error_message(self, values):

        if values["valtdyn"] is None:
            values["valtdyn"] = 0

        if values["valtdynb"] is None:
            values["valtdynb"] = 0

        # if self.player.elicit_type == "slider":
        #     print("Moved: ", self.player.moved_slider)
        #     if self.player.moved_slider is 0 or self.player.moved_slider is None:
        #        return 'Sie müssen den Slider auf der grauen Linie setzen um ihre Auszahlung zu bestimmen.'

        if self.player.elicit_type == "ticket":
            if (values["valtdyn"] + values["valtdynb"]) != 100:
                return 'Sie müssen insgesamt genau 100 Tickets setzen.'

        if self.player.elicit_type == "choice":
            print("val now is: ", values["val_now"])
            if values["val_now"] is None:
                return 'Sie müssen eine der drei Möglichkeiten auswählen.'

    def is_displayed(self):

        # don't display if timeout
        if self.participant.vars['expiry'] - time.time() > 3:
            False

        # show page if not yet finished
        if self.player.id_in_group == 1:
            return False
        else:
            if self.player.dynamic_end is False:
                return True #(self.player.treatment + self.round_number) % 3 == 1
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
                self.player.x = 1 - self.player.val_slider_dyn / 100
                self.player.val_slider_dyn = None

            # moved slider back to default 0
            # self.player.moved_slider = 0

            # adapt bounders upper and lower mixing
            if self.player.x == 0:
               print("new lower:", self.player.q_now)
               self.player.mix_lower = self.player.q_now
            if self.player.x == 1:
                print("new upper:", self.player.q_now)
                self.player.mix_upper = self.player.q_now

            # round choice
            self.player.x = round(self.player.x, ndigits=2)

            # safe choice if selected for payoff
            if self.participant.vars['payoff_title'] == self.group.title:
                if self.player.dyn_round <= self.participant.vars['payoff_number']:
                    print("SAFE FOR OUTPUT - normal")
                    print(self.player.x, self.player.q_now)
                    self.participant.vars['money'] = self.player.prize
                    print("XXX_money:", self.player.prize)
                    self.participant.vars['epoints'] = 100 * self.player.q_now / 10 * self.player.x
                    print("XXX_epoints:", self.participant.vars['epoints'])
                    self.participant.vars['cpoints'] = 100 * (1 - self.player.q_now / 10) * (1 - self.player.x)
                    print("XX_cpoints:", self.participant.vars['cpoints'])
                    self.participant.vars['e'] = Constants.etext[self.round_number - 1]
                    print("XXX_e:", self.participant.vars['e'])
                    self.participant.vars['c'] = Constants.ctext[self.round_number - 1]
                    print("XX_c", self.participant.vars['c'])

            # safe full situation in String
            self.player.dyn_all = self.player.dyn_all + " | " + str(self.player.q_now) + "," + str(self.player.x)

            # assign new q_now
            self.player.q_now = self.player.get_q_now()
            print("Just assigned q_now:", self.player.q_now)

            # safe choice if ends before selected for payoff
            if self.participant.vars['payoff_title'] == self.group.title:
                if self.player.dynamic_end:
                    if 'money' not in self.participant.vars:
                        print("SAFE FOR OUTPUT - because it ended before the round!")
                        self.participant.vars['money'] = self.player.prize
                        print("XXX_money:", self.player.prize)
                        self.participant.vars['epoints'] = 100 * self.player.q_now / 10 * self.player.x
                        print("XXX_epoints:", self.participant.vars['epoints'])
                        self.participant.vars['cpoints'] = 100 * (1 - self.player.q_now / 10) * (1 - self.player.x)
                        print("XX_cpoints:",  self.participant.vars['cpoints'])
                        self.participant.vars['e'] = Constants.etext[self.round_number - 1]
                        print("XXX_e:", self.participant.vars['e'])
                        self.participant.vars['c'] = Constants.ctext[self.round_number - 1]
                        print("XX_c", self.participant.vars['c'])

            # set starting value for next dynamic to NA
            self.player.val_now = None



class ticketsPage(Page):
    form_model = 'player'
    form_fields = ['valt0', 'valt1', 'valt2', 'valt3', 'valt4',
                   'valt5', 'valt6', 'valt7', 'valt8',
                   'valt0b', 'valt1b', 'valt2b', 'valt3b', 'valt4b',
                   'valt5b', 'valt6b', 'valt7b', 'valt8b'
                   ]

    def vars_for_template(self):
        return {
                'cur_round': self.round_number-1
                }

    def is_displayed(self):
        if self.player.id_in_group == 1:
            return False
        else:
            return (self.player.treatment + self.round_number) % 3 == 2

    def error_message(self, values):
        print('values is', values)
        if values["valt0"] + values["valt0b"] != 100:
            return 'Sie müssen für die Quote 90:10 genau 100 Tickets setzen.'
        if values["valt1"] + values["valt1b"] != 100:
            return 'Sie müssen für die Quote 80:20 genau 100 Tickets setzen.'
        if values["valt2"] + values["valt2b"] != 100:
            return 'Sie müssen für die Quote 70:30 genau 100 Tickets setzen.'
        if values["valt3"] + values["valt3b"] != 100:
            return 'Sie müssen für die Quote 60:40 genau 100 Tickets setzen.'
        if values["valt4"] + values["valt4b"] != 100:
            return 'Sie müssen für die Quote 50:50 genau 100 Tickets setzen.'
        if values["valt5"] + values["valt5b"] != 100:
            return 'Sie müssen für die Quote 40:60 genau 100 Tickets setzen.'
        if values["valt6"] + values["valt6b"] != 100:
            return 'Sie müssen für die Quote 30:70 genau 100 Tickets setzen.'
        if values["valt7"] + values["valt7b"] != 100:
            return 'Sie müssen für die Quote 20:80 genau 100 Tickets setzen.'
        if values["valt8"] + values["valt8b"] != 100:
            return 'Sie müssen für die Quote 10:90 genau 100 Tickets setzen.'

    def before_next_page(self):
        self.player.payoffq = random.choice(range(0, 8))
        self.player.x = getattr(self.player, 'valt{}'.format(self.player.payoffq))/100


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

        if self.participant.vars['payoff_title'] == self.group.title:
            self.session.vars['true_event'] = Constants.etext[self.round_number-1] if self.group.eventTRUE else Constants.ctext[self.round_number-1]
            self.session.vars['eventTRUE'] = self.group.eventTRUE
            print("XXX: true_event set to", self.session.vars['true_event'])



class Results(Page):
    def is_displayed(self):
        return self.player.id_in_group is not 1

    def vars_for_template(self):
        return {
            'etext': Constants.etext_short[self.round_number-1],
            'ctext': Constants.ctext_short[self.round_number - 1],
        }


    def before_next_page(self):
        if self.participant.vars['payoff_title'] == self.group.title:
            if 'epoints' not in self.participant.vars:
                print("WARNING: EPOINTS NOT GIVEN")
                self.participant.vars['epoints'] = 100
                self.participant.vars['cpoints'] = 100
            self.participant.vars['points_lot'] = self.participant.vars['epoints'] if self.session.vars['eventTRUE'] else self.participant.vars['cpoints']
            print("XXX_points_lot - FINAL POINTS are:", self.participant.vars['points_lot'])


page_sequence = [
    AllGroupsWaitPage,
    explanation,
    #ticketsPage,
    #sliderPage,
    #choicePage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    dynamicPage,
    input,
    AllGroupsWaitPage,
    Results,
]
