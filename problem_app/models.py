from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Philipp Chapkovski, chapkovski@gmail.com'

doc = """
An app to test your skills on making the code DRY
"""


class Constants(BaseConstants):
    name_in_url = 'problem_app'
    players_per_group = 2
    num_rounds = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trustor_decision = models.IntegerField(max=100,
                                           verbose_name='Make your decision as a trustor')
    trustor_beliefs = models.IntegerField(max=100,
                                          verbose_name='How much (as %%) do you believe trustee send you back?')
    trustee_decision = models.IntegerField(max=100,
                                           verbose_name='Make your decision as a trustee')
    trustee_beliefs = models.IntegerField(max=100,
                                          verbose_name='How much  do you believe trustor send you?')
    political_views = models.IntegerField(choices=[(0, 'Left'),
                                                   (1, 'Right')],
                                          widget=widgets.RadioSelect)
    trust = models.IntegerField(choices=[
        (0, 'You can trust most people.'),
        (1, 'You can never be too careful with others.'),
    ],
        widget=widgets.RadioSelect
    )
    experimenter_demand = models.LongStringField(verbose_name='What do you think this experiment was about?')
    gender = models.IntegerField(
        choices=[(0, 'Female'),
                 (1, 'Male')],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'
