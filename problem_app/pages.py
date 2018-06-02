from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player


class Results(Page):
    def is_displayed(self):
        if self.player.role() == 'A':
            trustee = self.group.get_player_by_role('B')
            self.player.payoff = 100 - self.player.trustor_decision + trustee.trustee_decision / 100 * self.player.trustor_decision
        else:
            trustor = self.group.get_player_by_role('A')
            self.player.payoff = trustor.trustor_decision * 2 - self.player.trustee_decision / 100 * trustor.trustor_decision
        return True


class Intro1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Intro2(Page):
    def is_displayed(self):
        return self.round_number == 1


class ControlQuestions1(Page):
    def is_displayed(self):
        return self.round_number == 1


class ControlQuestions2(Page):
    def is_displayed(self):
        return self.round_number == 1


# by the rules of the game in T1 a player A takes the decision first, and a Plaayer B waits.
# Then player B makes decisions observing player A's decisions
# in T2 it's vice versa: first decisino are made by player B, and then Player A observing decisions of Player b makes
# the choice
class Decision1(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'A'
        else:
            return self.player.role() == 'B'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['trustor_decision']
        else:
            return ['trustee_decision']


class Decision2(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'A'
        else:
            return self.player.role() == 'B'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['trustor_beliefs']
        else:
            return ['trustee_beliefs']


class Decision3(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'B'
        else:
            return self.player.role() == 'A'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['trustee_decision']
        else:
            return ['trustor_decision']

    def vars_for_template(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            trustor = self.group.get_player_by_role('A')
            decision_text = 'The trustor decided to send  {} of his endowment'.format(
                trustor.trustor_decision)
            belief_text = 'The trustor believes you will send him back  {}% '.format(
                trustor.trustor_beliefs)
            return {
                'decision_text': decision_text,
                'belief_text': belief_text,
            }
        else:
            trustee = self.group.get_player_by_role('B')
            decision_text = 'The trustee decided to send back  {}% of what you will send to him/her'.format(
                trustee.trustee_decision)
            belief_text = 'The trustee believes you will send him/her {}'.format(
                trustee.trustee_beliefs)
            return {
                'decision_text': decision_text,
                'belief_text': belief_text,
            }


class Decision4(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'B'
        else:
            return self.player.role() == 'A'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['trustee_beliefs']
        else:
            return ['trustor_beliefs']

    def vars_for_template(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            trustor = self.group.get_player_by_role('A')
            decision_text = 'The trustor decided to send  {} of his endowment'.format(
                trustor.trustor_decision)
            belief_text = 'The trustor believes you will send him back  {}% '.format(
                trustor.trustor_beliefs)
            return {
                'decision_text': decision_text,
                'belief_text': belief_text,
            }
        else:
            trustee = self.group.get_player_by_role('B')
            decision_text = 'The trustee decided to send back  {}% of what you will send to him/her'.format(
                trustee.trustee_decision)
            belief_text = 'The trustee believes you will send him/her {}'.format(
                trustee.trustee_beliefs)
            return {
                'decision_text': decision_text,
                'belief_text': belief_text,
            }


class Survey1(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def get_form_fields(self):
        a = ['political_views', 'trust']
        b = ['experimenter_demand', 'gender']
        import random
        rand = random.random()
        if rand < .5:
            random.shuffle(a)
            return a
        else:
            random.shuffle(b)
            return b


class Survey2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def get_form_fields(self):
        a = ['political_views', 'trust']
        b = ['experimenter_demand', 'gender']
        import random
        if self.player.trust is None:
            random.shuffle(a)
            return a
        else:
            random.shuffle(b)
            return b


page_sequence = [
    Intro1,
    Intro2,
    ControlQuestions1,
    ControlQuestions2,
    Decision1,
    Decision2,
    WaitPage,
    Decision3,
    Decision4,
    WaitPage,
    Results,
    Survey1,
    Survey2
]
