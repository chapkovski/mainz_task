from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Philipp Chapkovski, chapkovski@gmail.com'

doc = """
An app to test your skills on making the code DRY
"""


class Constants(BaseConstants):
    name_in_url = 'solution_app'
    players_per_group = 2
    num_rounds = 4
    endowment = 100
    multiplier = 2
    returning_max = 100  #(for percentage of amount received)
    treatments = ['T1', 'T2']
    decision_order = {'T1': ['sender', 'receiver'], 'T2': ['receiver', 'sender']}
    splitting_round = 3
    POLITICAL_CHOICES = [(0, 'Left'),
                         (1, 'Right')]

    GENDER_CHOICES = [(0, 'Female'),
                      (1, 'Male')]

    TRUST_CHOICES = [
        (0, 'You can trust most people.'),
        (1, 'You can never be too careful with others.'),
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        treatment_seq = self.session.config.get('treatment_seq', Constants.treatments)
        assert set(treatment_seq).issubset(Constants.treatments)
        for g in self.get_groups():
            if self.round_number < Constants.splitting_round:
                g.treatment = treatment_seq[0]
            else:
                g.treatment = treatment_seq[1]


class Group(BaseGroup):
    treatment = models.StringField()
    sender_decision = models.IntegerField(max=Constants.endowment,
                                          verbose_name='Make your decision as a sender')
    sender_beliefs = models.IntegerField(max=Constants.returning_max,
                                         verbose_name='How much (as %%) do you believe a Receiver sends you back?')
    receiver_decision = models.IntegerField(max=Constants.returning_max,
                                            verbose_name='Make your decision as a Receiver (in %%)')
    receiver_beliefs = models.IntegerField(max=Constants.endowment,
                                           verbose_name='How much  do you believe you will get from the Sender?')

    def set_payoffs(self):
        sender = self.get_player_by_role('sender')
        receiver = self.get_player_by_role('receiver')
        share_back = self.receiver_decision * Constants.multiplier / 100 * self.sender_decision
        sender.payoff = Constants.endowment - self.sender_decision + share_back
        receiver.payoff = self.sender_decision * Constants.multiplier - share_back


class Player(BasePlayer):
    political_views = models.IntegerField(choices=Constants.POLITICAL_CHOICES,
                                          widget=widgets.RadioSelect)
    trust = models.IntegerField(choices=Constants.TRUST_CHOICES,
                                widget=widgets.RadioSelect
                                )
    experimenter_demand = models.LongStringField(verbose_name='What do you think this experiment was about?')
    gender = models.IntegerField(
        choices=Constants.GENDER_CHOICES,
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect)

    def role(self):
        if self.id_in_group == 1:
            return 'sender'
        else:
            return 'receiver'
