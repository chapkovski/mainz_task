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
    trustor_decision = models.IntegerField()
    trustor_beliefs = models.IntegerField()
    trustee_decision = models.IntegerField()
    trustee_beliefs = models.IntegerField()
    political_views = models.IntegerField()
    trust = models.IntegerField()
    experimenter_demand = models.StringField()
    belief = models.IntegerField()

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'
