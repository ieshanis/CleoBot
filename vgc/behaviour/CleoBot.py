#GroupWork by Eshani Sharma and Cyrus Mathew

from vgc.behaviour import BattlePolicy
from vgc.behaviour import TeamBuildPolicy
from vgc.behaviour import CleoBattlePolicy
from vgc.behaviour import CleoBuildPolicy
from vgc.competition.Competitor import Competitor

class CleoBot(Competitor):
    def _init_(self, name: str = "CleoBot"):
        self._name = name
        self.my_battle_policy = CleoBattlePolicy()
        self.my_team_build_policy = CleoBuildPolicy()

    @property
    def battle_policy(self) -> BattlePolicy:
        return self.my_battle_policy

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self.my_team_build_policy

    @property
    def name(self):
        return self._name
