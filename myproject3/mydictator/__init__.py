import random
from otree.api import *

doc = """
One player decides how to divide a certain amount between himself and the other player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986): S285-S300.
"""

class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        label="I will keep",
    )

    endowment = models.CurrencyField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endowment = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = group.endowment - group.kept

class Introduction(Page):
    pass

class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.group.kept = 0


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(offer=group.endowment - group.kept)

page_sequence = [Introduction, Offer, ResultsWaitPage, Results]
