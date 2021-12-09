from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random
import time
import math


class firstPage(Page):

    def is_displayed(self):
        return self.player.participant.vars['participant']

    def before_next_page(self):

        if self.player.round_number is 1:
            print(len(Constants.title),[i for i in range(0,len(Constants.title))])
            self.player.participant.vars['topic_order'] = random.sample([i for i in range(0, len(Constants.title))], len(Constants.title))
            print('topic order is ', self.player.participant.vars['topic_order'])

            # start time of urns app
            self.participant.vars['slider_expiry'] = time.time() + Constants.slider_minutes * 60

        self.player.topic_number = math.floor((self.round_number-1)/2)+1

        # assign topic
        self.player.topic = self.player.participant.vars['topic_order'][self.player.topic_number-1]

        # choose elicitation type
        self.player.elicit_type = Constants.elicit_types[(self.player.round_number + 1) % 2]
        print("elicit type is ", self.player.elicit_type)

        # randomize prize money by id
        self.player.prize = "10 Euro" # if ((self.player.id_in_group + self.player.round_number) % 2 is 1) else "20 Euro"

        self.player.title = self.player.fun_title()
        self.player.dyn_round = 0
        self.player.dynamic_end = False


        # randomly choose order of questions
        self.player.participant.vars['q'] = random.sample(Constants.a, len(Constants.a))
        self.player.participant.vars['q_free'] = self.player.participant.vars['q']
        print("the list of qs is", self.player.participant.vars['q'])

        # assign new q_now
        self.player.assign_q()

        options = self.player.make_text_dynamic()
        random.shuffle(options)
        self.player.choices_order = self.player.choices_order + str(options)
        self.player.participant.vars['options'] = options

        # don't display if slider and slow before
        if self.player.elicit_type=="slider":
            print("-------TIME left: ", self.participant.vars['slider_expiry'] - time.time())
            if self.participant.vars['slider_expiry'] - time.time() < 0:
                print("TIME OUT FOR SLIDER: set dynamic end to True")
                self.player.dynamic_end = True

            # skip slider if not gepunkteter Ball
            print("check slider for topic, which is now ", self.player.title)
            print(self.player.title == "gepunkteter Ball aus Urne")
            if self.player.title == "gepunkteter Ball aus Urne":
                print("true for gepunktet")
                self.player.dynamic_end = False
            else:
                print("Set dynamic end on true")
                self.player.dynamic_end = True

        # start time out time
        self.participant.vars['expiry'] = time.time() + Constants.minutes * 60



class explanation(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.elicit_type!= "slider"

    def vars_for_template(self):
        return {
                'topic': self.player.topic,
                'treatment': self.player.treatment,
                'image_path': '{}.jpeg'.format(self.player.fun_title()),
                }






class dynamicPage(Page):
    form_model = 'player'
    form_fields = ['val_now',
                   'val_first',
                   "val_slider_dyn",
                   'checkslider',
                   ]

    def vars_for_template(self):
        return {
                'round_number': self.round_number-1,
                'q_now': int(round(self.player.q_now * 10)),
                'q_not_now': int(round(self.player.qnot_now * 10)),
                'prize_string': self.player.prize,
                'quote_e': int(round(10*self.player.q_now)),
                'quote_c': int(round(10*self.player.qnot_now)),
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

    def val_now_error_message(self, value):
        if not value and self.player.elicit_type == "choice":
            return 'Bitte wählen Sie eine Option.'


    def val_first_error_message(self, value):
        if not value and self.player.elicit_type == "choice_twice":
            return 'Bitte wählen Sie eine Option.'


    def val_now_choices(self):
        options = self.player.make_text_dynamic()
        random.shuffle(options)
        self.player.choices_order = self.player.choices_order + str(options)
        return options


    def val_first_choices(self):
        options = self.player.make_text_dynamic()
        options = [options[1], options[2]]
        random.shuffle(options)
        return(options)




    def is_displayed(self):

        # show page if not yet finished
        if self.player.participant.vars['participant'] == False:
            return False


        print(self.participant.vars['expiry'] - time.time())
        # don't display if timeout
        if self.participant.vars['expiry'] - time.time() < 3:
            return False


        if self.player.dynamic_end:
            return False
        else:
            return True

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def before_next_page(self):

        if not self.timeout_happened:

            if self.player.elicit_type == "choice":
                response = getattr(self.player, 'val_now')
                self.player.x = \
                    0 if response == "C" \
                        else 1 if response == "E" \
                        else 1 - self.player.q_intern / 10

                self.player.val_now = None



            if self.player.elicit_type == "slider":
                self.player.x = 1 - self.player.val_slider_dyn / 100
                self.player.val_slider_dyn = None

            if self.player.elicit_type != "choice_twice":
                # adapt bounds for upper and lower mixing
                if self.player.x == 0:
                   print("new lower:", self.player.q_intern)
                   self.player.mix_lower = self.player.q_intern
                elif self.player.x == 1:
                    print("new upper:", self.player.q_intern)
                    self.player.mix_upper = self.player.q_intern

                # round choice
                self.player.x = round(self.player.x, ndigits=2)

                # safe choice if selected for payoff
                if self.session.vars['payoff_title'] == self.player.title:
                    if self.player.dyn_round <= self.session.vars['payoff_number']:
                        print("SAFE FOR OUTPUT as chosen title is ", self.session.vars["payoff_title"])
                        print("x: ", self.player.x, " q:", self.player.q_intern)
                        self.participant.vars['money'] = self.player.prize
                        print("XXX_money:", self.player.prize)
                        self.participant.vars['epoints'] = 100 * self.player.q_now / 10 * self.player.x
                        print("XXX_epoints:", self.participant.vars['epoints'])
                        self.participant.vars['cpoints'] = 100 * self.player.qnot_now / 10 * (1 - self.player.x)
                        print("XX_cpoints:", self.participant.vars['cpoints'])
                        self.participant.vars['e'] = self.player.fun_etext()
                        print("XXX_e:", self.participant.vars['e'])
                        self.participant.vars['c'] = self.player.fun_ctext()
                        print("XX_c", self.participant.vars['c'])

                # safe full situation in String
                self.player.dyn_all = self.player.dyn_all + " | " + str(self.player.q_intern) + "," + str(self.player.x)

                # assign new q_now
                self.player.assign_q()


            # set starting value for next dynamic to NA
            self.player.val_now = None


class dynamicPage2(Page):
    form_model = 'player'
    form_fields = ['val_second',
                   ]

    def vars_for_template(self):

        return {
                'round_number': self.round_number-1,
                'dynamic_counter': self.player.dyn_round,
                'image_path': '{}.jpeg'.format(self.player.fun_title()),
                'image_pathE': '{}.jpeg'.format("E_" + self.player.fun_title()),
                'image_pathC': '{}.jpeg'.format("C_" + self.player.fun_title()),
        }

    def val_second_choices(self):
        options = self.player.make_text_dynamic()
        if self.player.val_first == "E":
            options = [options[0],options[1]]
        elif self.player.val_first == "C":
            options = [options[0],options[2]]
        else:
            options = [options[2],options[1]]
        random.shuffle(options)
        return options

    def val_second_error_message(self, value):
        if not value and self.player.elicit_type == "choice_twice":
            return 'Bitte wählen Sie eine Option.'

    def is_displayed(self):

        if self.player.elicit_type != "choice_twice":
            return False

        # show page if not yet finished
        if self.player.participant.vars['participant'] == False:
            return False

        # don't display if timeout
        if self.participant.vars['expiry'] - time.time() < 3:
            print("Timeout")
            return False


        if self.player.dynamic_end:
            print("Dynamic end")
            return False
        else:
            return True


    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def before_next_page(self):

        if not self.timeout_happened:

            response = getattr(self.player, 'val_second')
            self.player.x = \
                0 if response == "C" \
                else 1 if response == "E" \
                else 1- self.player.q_intern/10

            self.player.val_second = None
            self.player.val_first = None


            # adapt bounds for upper and lower mixing
            if self.player.x == 0:
               print("new lower:", self.player.q_intern)
               self.player.mix_lower = self.player.q_intern
            elif self.player.x == 1:
                print("new upper:", self.player.q_intern)
                self.player.mix_upper = self.player.q_intern

            # round choice
            self.player.x = round(self.player.x, ndigits=2)

            # safe choice if selected for payoff
            if self.session.vars['payoff_title'] == self.player.title:
                if self.player.dyn_round <= self.session.vars['payoff_number']:
                    print("SAFE FOR OUTPUT as chosen title is ", self.session.vars["payoff_title"])
                    print("x: ", self.player.x, " q:", self.player.q_intern)
                    self.participant.vars['money'] = self.player.prize
                    print("XXX_money:", self.player.prize)
                    self.participant.vars['epoints'] = 100 * self.player.q_now / 10 * self.player.x
                    print("XXX_epoints:", self.participant.vars['epoints'])
                    self.participant.vars['cpoints'] = 100 * self.player.qnot_now / 10 * (1 - self.player.x)
                    print("XX_cpoints:", self.participant.vars['cpoints'])
                    self.participant.vars['e'] = self.player.fun_etext()
                    print("XXX_e:", self.participant.vars['e'])
                    self.participant.vars['c'] = self.player.fun_ctext()
                    print("XX_c", self.participant.vars['c'])

            # safe full situation in String
            self.player.dyn_all = self.player.dyn_all + " | " + str(self.player.q_intern) + "," + str(self.player.x)

            # assign new q_now
            self.player.assign_q()


page_sequence = [
    firstPage,
    explanation,
    dynamicPage,
    dynamicPage2,
    dynamicPage,
    dynamicPage2,
    dynamicPage,
    dynamicPage2,
    dynamicPage,
    dynamicPage2,
    dynamicPage,
    dynamicPage2,
]
