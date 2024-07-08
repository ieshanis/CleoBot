#GroupWork by Eshani Sharma and Cyrus Mathew

import random
from typing import List

from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Objects import PkmFullTeam, PkmRoster
from vgc.balance.meta import MetaData
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE
from vgc.datatypes.Types import PkmType

class CleoBuildPolicy(TeamBuildPolicy):
    """
    Agent that builds a balanced team with diverse roles and types.
    """

    def __init__(self):
        self.roster = None

    def set_roster(self, roster: PkmRoster, ver: int = 0):
        self.roster = roster

    def get_action(self, meta: MetaData) -> PkmFullTeam:
        # Ensure the roster is not empty and contains enough Pokémon
        if not self.roster or len(self.roster) < DEFAULT_PARTY_SIZE:
            raise ValueError("Roster must contain at least 6 Pokémon.")

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

        # Step 2: Select Pokémon to form a balanced team
        team = []

        # Ensure we have at least one of each type
        if offensive:
            team.append(random.choice(offensive))
        if defensive:
            team.append(random.choice(defensive))
        if support:
            team.append(random.choice(support))

        # Fill the rest of the team randomly to ensure we have 6 Pokémon
        while len(team) < DEFAULT_PARTY_SIZE:
            candidate = random.choice(self.roster)
            if candidate not in team:
                team.append(candidate)

        # Step 3: Assign moves to each Pokémon ensuring no duplication and all moves are valid
        full_team = []
        for pt in team:
            moves = random.sample(pt.move_roster, min(DEFAULT_PKM_N_MOVES, len(pt.move_roster)))
            full_team.append(pt.gen_pkm(moves))

        return PkmFullTeam(full_team)
