"""facade_logic.py: An interface for other software the wishes to run games of indirect reciprocity"""

__author__ = "James King"

from .community_logic import Community
from .observation_logic import ActionObserver, PlayerObserver, Observer
from .action_logic import Action, InteractionAction
from typing import List, Dict
from .strategy_logic import Strategy


class Results:

    def __init__(self, community: Community):
        self._action_observer = ActionObserver(community.get_id())
        self._player_observer = PlayerObserver(community.get_id())
        self._observers: List[Observer] = [self._action_observer, self._player_observer]
        self._community = community
        self._populations: List[Dict[int, List]] = []

    @property
    def generations(self) -> List[int]:
        return self._action_observer.generations

    @property
    def players(self) -> Dict[int, List[int]]:
        return self._action_observer.players

    @property
    def observers(self) -> List[Observer]:
        return self._observers

    @property
    def actions(self) -> Dict[int, List[Action]]:
        return self._action_observer.actions

    @property
    def actions_by_generation(self) -> Dict[int, Dict[int, List[Action]]]:
        return self._action_observer.actions_by_generation

    @property
    def actions_by_generation_and_player(self) -> Dict[int, Dict[int, Dict[int, Action]]]:
        return self._action_observer.actions_by_generation_and_player

    @property
    def interactions(self) -> Dict[int, InteractionAction]:
        return self._action_observer.interactions

    @property
    def interactions_by_generation(self) -> Dict[int, Dict[int, List[InteractionAction]]]:
        return self._action_observer.interactions_by_generation

    @property
    def interactions_by_generation_and_player(self) -> Dict[int, Dict[int, Dict[int, InteractionAction]]]:
        return self._action_observer.interactions_by_generation_and_player

    @property
    def cooperation_rate(self) -> int:
        return self._action_observer.cooperation_rate

    @property
    def cooperation_rate_by_generation(self) -> Dict[int, int]:
        return self._action_observer.cooperation_rate_by_generation

    @property
    def cooperation_rate_by_generation_and_player(self) -> Dict[int, Dict[int, int]]:
        return self._action_observer.cooperation_rate_by_generation_and_player

    @property
    def social_activeness(self) -> int:
        return self._action_observer.social_activeness

    @property
    def social_activeness_by_generation(self) -> Dict[int, int]:
        return self._action_observer.social_activeness_by_generation

    @property
    def social_activeness_by_generation_and_player(self) -> Dict[int, Dict[int, int]]:
        return self._action_observer.social_activeness_by_generation_and_player

    @property
    def positivity_of_gossip_percentage(self) -> int:
        return self._action_observer.positivity_of_gossip_percentage

    @property
    def positivity_of_gossip_percentage_by_generation(self) -> Dict[int, int]:
        return self._action_observer.positivity_of_gossip_percentage_by_generation

    @property
    def positivity_of_gossip_percentage_by_generation_and_player(self) -> Dict[int, Dict[int, int]]:
        return self._action_observer.positivity_of_gossip_percentage_by_generation_and_player

    @property
    def corrupted_observations(self) -> bool:
        for observer in self._observers:
            if observer.corrupted_observations:
                return True
        return False

    @property
    def community_fitness(self) -> int:
        return self._player_observer.community_fitness

    @property
    def fitness_by_generation(self) -> Dict[int, int]:
        return self._player_observer.fitness_by_generation

    @property
    def fitness_by_generation_and_player(self) -> Dict[int, Dict[int, int]]:
        return self._player_observer.fitness_by_generation_and_player

    @property
    def populations(self) -> List[Dict[Strategy, int]]:
        return self._community.get_strategy_count_by_generation()

    @property
    def id_to_strategy_map(self) -> Dict[int, Dict[int, Strategy]]:
        map: Dict = {}
        for gen in self._community.get_generations():
            map[gen.id] = {}
            for player in gen.get_players():
                map[gen.id][player.id] = player.strategy
        return map


class ReputationGame:

    def __init__(self, initial_strategies: List[Dict], num_of_onlookers: int = 5, num_of_generations: int = 10,
                 length_of_generations: int = 30, mutation_chance: float = 0):
        self._initial_strategies = initial_strategies
        print(initial_strategies)
        self._num_of_onlookers = num_of_onlookers
        self._num_of_generations = num_of_generations
        self._length_of_generations = length_of_generations
        self._mutation_chance = mutation_chance

    @property
    def initial_strategies(self) -> List[Dict]:
        return self._initial_strategies

    @property
    def num_of_onlookers(self) -> int:
        return self._num_of_onlookers

    @property
    def num_of_generations(self) -> int:
        return self._num_of_generations

    @property
    def length_of_generations(self) -> int:
        return self._length_of_generations

    @property
    def mutation_chance(self) -> float:
        return self._mutation_chance

    def run(self) -> Results:
        community_strategies: Dict[Strategy, int] = {}
        for strategy in self._initial_strategies:
            generated_strategy: Strategy = Strategy(strategy['name'], strategy['options'])
            if generated_strategy in community_strategies:
                community_strategies[generated_strategy] += strategy['count']
            else:
                community_strategies[generated_strategy] = strategy['count']
        community = Community(community_strategies, num_of_onlookers=self._num_of_onlookers,
                              num_of_generations=self._num_of_generations,
                              length_of_generations=self._length_of_generations,
                              mutation_chance=self._mutation_chance)
        results = Results(community)
        community.extend_observers(results.observers)
        community.simulate()
        return results

