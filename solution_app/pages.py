from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player
import json
import random

class FirstPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class SurveyPage(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Intro1(FirstPage):
    ...


class Intro2(FirstPage):
    ...
 

class ControlQuestions1(FirstPage):
    ...


class ControlQuestions2(FirstPage):
    ...


# by the rules of the game in T1 a player A takes the decision first, and a Plaayer B waits.
# Then player B makes decisions observing player A's decisions
# in T2 it's vice versa: first decisino are made by player B, and then Player A observing decisions of Player b makes
# the choice
class DecisionBelief(Page):
    form_model = 'group'
    own_field = None

    def get_order(self):
        order = int(self.__class__.__name__.split('_')[1])
        return int(order) - 1

    def is_displayed(self):
        r = self.player.role()
        i = self.get_order()
        return self.player.role() == Constants.decision_order[self.group.treatment][i]

    def get_form_fields(self):
        return ['{}_{}'.format(self.player.role(), self.own_field), ]


class Decision_1(DecisionBelief):
    own_field = 'decision'


class Belief_1(DecisionBelief):
    own_field = 'beliefs'


class Belief_2(DecisionBelief):
    own_field = 'beliefs'


class Decision_2(DecisionBelief):
    own_field = 'decision'

    def vars_for_template(self):
        if self.group.treatment == 'T1':
            decision_text = 'The trustor decided to send  {} of his endowment'.format(
                self.group.sender_decision)
            belief_text = 'The trustor believes you will send him back  {}% '.format(
                self.group.sender_beliefs)
        else:
            decision_text = 'The trustee decided to send back  {}% of what you will send to him/her'.format(
                self.group.receiver_decision)
            belief_text = 'The trustee believes you will send him/her {}'.format(
                self.group.receiver_beliefs)
        return {
            'decision_text': decision_text,
            'belief_text': belief_text,
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    ...


class Survey1(SurveyPage):
    def get_form_fields(self):
        return json.loads(self.player.qs_order)[0]


class Survey2(SurveyPage):
    def get_form_fields(self):
        return json.loads(self.player.qs_order)[1]


page_sequence = [
    # Intro1,
    # Intro2,
    # ControlQuestions1,
    # ControlQuestions2,
    # Decision_1,
    # Belief_1,
    # WaitPage,
    # Belief_2,
    # Decision_2,
    # ResultsWaitPage,
    # Results,
    Survey1,
    Survey2
]
