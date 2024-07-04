from vgc.behaviour import BattlePolicy
from vgc.datatypes.Constants import DEFAULT_PKM_N_MOVES, DEFAULT_PARTY_SIZE, TYPE_CHART_MULTIPLIER
from vgc.datatypes.Objects import GameState
from vgc.datatypes.Types import PkmStat, PkmType, WeatherCondition
import numpy as np
from typing import List

def estimate_damage(move_type: PkmType, pkm_type: PkmType, move_power: float, opp_pkm_type: PkmType,
                    attack_stage: int, defense_stage: int, weather: WeatherCondition) -> float:
    stab = 1.5 if move_type == pkm_type else 1.
    if (move_type == PkmType.WATER and weather == WeatherCondition.RAIN) or (
            move_type == PkmType.FIRE and weather == WeatherCondition.SUNNY):
        weather = 1.5
    elif (move_type == PkmType.WATER and weather == WeatherCondition.SUNNY) or (
            move_type == PkmType.FIRE and weather == WeatherCondition.RAIN):
        weather = .5
    else:
        weather = 1.
    stage_level = attack_stage - defense_stage
    stage = (stage_level + 2.) / 2 if stage_level >= 0. else 2. / (np.abs(stage_level) + 2.)
    damage = TYPE_CHART_MULTIPLIER[move_type][opp_pkm_type] * stab * weather * stage * move_power
    return damage

class TypePolicy(BattlePolicy):
    """
    Battle policy that selects actions based on a heuristic combining type effectiveness and HP.
    """

    def get_action(self, g: GameState) -> int:
        # get weather condition
        weather = g.weather.condition

        # get my team
        my_team = g.teams[0]
        my_active = my_team.active
        my_attack_stage = my_team.stage[PkmStat.ATTACK]
        my_hp = my_active.hp

        # get opponent team
        opp_team = g.teams[1]
        opp_active = opp_team.active
        opp_active_type = opp_active.type
        opp_defense_stage = opp_team.stage[PkmStat.DEFENSE]
        opp_hp = opp_active.hp

        # Calculate damage for each move
        damage: List[float] = []
        for move in my_active.moves:
            damage.append(estimate_damage(move.type, my_active.type, move.power, opp_active_type,
                                          my_attack_stage, opp_defense_stage, weather))

        # Select the move with the highest damage
        move_id = int(np.argmax(damage))

        # If the damage can knock out the opponent, use that move
        if damage[move_id] >= opp_hp:
            return move_id

        # If my active Pokémon has low HP, consider switching to a different Pokémon
        if my_hp < 0.3 * my_active.max_hp:
            match_up: List[float] = []
            not_fainted = False
            for pkm in my_team.party:
                if pkm.hp == 0.0:
                    match_up.append(2.0)  # Fainted Pokémon
                else:
                    not_fainted = True
                    match_up.append(TYPE_CHART_MULTIPLIER[pkm.type][opp_active_type])

            if not_fainted:
                return int(np.argmin(match_up)) + DEFAULT_PKM_N_MOVES

        # Otherwise, use the move with the highest damage
        return move_id