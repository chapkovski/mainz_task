from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player


class Results(Page):
    def is_displayed(self):
        if self.player.role() == 'sender':
            receiver = self.group.get_player_by_role('receiver')
            self.player.payoff = 100 - self.player.sender_decision + receiver.receiver_decision / 100 * self.player.sender_decision
        else:
            sender = self.group.get_player_by_role('sender')
            self.player.payoff = sender.sender_decision * 2 - self.player.receiver_decision / 100 * sender.sender_decision * 2
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
            return self.player.role() == 'sender'
        else:
            return self.player.role() == 'receiver'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['sender_decision']
        else:
            return ['receiver_decision']


class Decision2(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'sender'
        else:
            return self.player.role() == 'receiver'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['sender_beliefs']
        else:
            return ['receiver_beliefs']





class Decision3(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'receiver'
        else:
            return self.player.role() == 'sender'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['receiver_beliefs']
        else:
            return ['sender_beliefs']


class Decision4(Page):
    form_model = 'player'

    def is_displayed(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return self.player.role() == 'receiver'
        else:
            return self.player.role() == 'sender'

    def get_form_fields(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            return ['receiver_decision']
        else:
            return ['sender_decision']

    def vars_for_template(self):
        treatmentseq = self.session.config['treatment_seq']
        curtreatment = treatmentseq[self.round_number - 1]
        if curtreatment == 'T1':
            sender = self.group.get_player_by_role('sender')
            decision_text = 'The sender decided to send  {} of his endowment'.format(
                sender.sender_decision)
            belief_text = 'The sender believes you will send him back  {}% '.format(
                sender.sender_beliefs)
            return {
                'decision_text': decision_text,
                'belief_text': belief_text,
            }
        else:
            receiver= self.group.get_player_by_role('receiver')
            decision_text = 'The receiver decided to send back  {}% of what you will send to him/her'.format(
                receiver.receiver_decision)
            belief_text = 'The receiver believes you will send him/her {}'.format(
                receiver.receiver_beliefs)
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
