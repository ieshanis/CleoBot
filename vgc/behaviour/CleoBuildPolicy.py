import random
from typing import List

from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Objects import Pkm, PkmTemplate, PkmFullTeam, PkmRoster
from vgc.balance.meta import MetaData
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES

class BalancedTeamBuilder(TeamBuildPolicy):
    """
    Agent that builds a -- balanced team with diverse roles and types.
    """

    def _init_(self):
        self.roster = None

    def set_roster(self, roster: PkmRoster, ver: int = 0):
        self.roster = roster

    def get_action(self, meta: MetaData) -> PkmFullTeam:
        # Ensure the roster is not empty
        if not self.roster or len(self.roster) < 3:
            raise ValueError("Roster must contain at least 3 Pokémon.")

        # Step 1: Categorize Pokémon by roles (offensive, defensive, support)
        offensive = []
        defensive = []
        support = []

        for pt in self.roster:
            # Simple heuristic based on HP, Attack, Defense stats to categorize roles
            if pt.base_stats.hp > 80 and pt.base_stats.defense > 80:
                defensive.append(pt)
            elif pt.base_stats.attack > 80 or pt.base_stats.special_attack > 80:
                offensive.append(pt)
            else:
                support.append(pt)

        # Step 2: Select one Pokémon from each category to form a balanced team
        team = []

        if offensive:
            team.append(random.choice(offensive))
        if defensive:
            team.append(random.choice(defensive))
        if support:
            team.append(random.choice(support))

        # If the team has fewer than 3 Pokémon, randomly select additional ones to fill the team
        while len(team) < 3:
            team.append(random.choice(self.roster))

        # Step 3: Assign moves to each Pokémon
        full_team = []
        for pt in team:
            moves = random.sample(range(len(pt.move_roster)), DEFAULT_PKM_N_MOVES)
            full_team.append(pt.gen_pkm(moves))

        return PkmFullTeam(full_team)