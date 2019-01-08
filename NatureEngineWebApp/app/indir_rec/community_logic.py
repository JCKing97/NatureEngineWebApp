"""community_logic.py: the module for functionality surrounding communities: reproduction,
simulation of a whole tournament,setup of a tournament etc."""

import requests
from flask import current_app
from typing import List, Dict
from .generation_logic import Generation
import random


class CommunityCreationException(Exception):
    """Exception generated when failed to create a community"""

    def __init__(self, message):
        super().__init__("Error creating community: " + message)


class Community:
    """A community encompasses a number of generations, a first generation is selected on construction, the next
    generations are then created using a reproduction algorithm"""

    def __init__(self, strategies: List[Dict], num_of_onlookers: int = 5, num_of_generations: int = 10,
                 length_of_generations: int = 30, mutation_chance: float = 0):
        """
        Set the parameters for the community and the initial set of players to simulate the community with
        :param strategies: The initial set of players to simulate the community
        :type strategies: List[Dict]
        :param num_of_onlookers: The number of onlookers for each interaction
        :type num_of_onlookers: int
        :param num_of_generations: The number of generations the simulation will run
        :type num_of_generations: int
        :param length_of_generations: The number of rounds each generation will run for
        :type length_of_generations: int
        """
        self._community_id = requests.request("POST", current_app.config['AGENTS_URL'] + 'community').json()['id']
        if num_of_onlookers <= 0:
            raise CommunityCreationException("number of onlookers <= 0")
        if length_of_generations <= 5:
            raise CommunityCreationException("length of generations <= 5")
        if num_of_generations <= 2:
            raise CommunityCreationException("number of generations <= 2")
        if mutation_chance > 1 or mutation_chance < 0:
            raise CommunityCreationException("mutation chance should be a probability between 0 and 1")
        self._mutation_chance: float = mutation_chance
        self._num_of_onlookers: int = num_of_onlookers
        self._num_of_generations: int = num_of_generations
        self._length_of_generations: int = length_of_generations
        self._first_strategies = strategies
        self._generations: List[Generation] = []
        self._current_time: int = 0
        self._generation_size: int = 0
        for strategy in strategies:
            self._generation_size += strategy['count']
        self._cooperation_count: int = 0
        self._interaction_count: int = 0
        self._cooperation_rate_by_generation: List[int] = []
        self._actions: List[List[Dict]] = []
        self._interactions: List[Dict] = []
        self._interactions_by_generation: List[List[Dict[str]]] = []
        self._social_welfare: int = 0
        self._social_welfare_by_generation: List[int] = []
        self._social_action_count: int = 0
        self._idle_action_count: int = 0
        self._non_donor_action_count: int = 0
        self._fitness: int = 0
        self._strategy_count_by_generation: List[List[Dict[str]]] = []

    def get_id(self) -> int:
        """
        Get the id of the community
        :return: The id on the community
        :rtype: int
        """
        return self._community_id

    def get_num_of_onlookers(self) -> int:
        """
        Get the number of onlookers for each interaction in this community
        :return: The number of onlooker for each interaction
        :rtype: int
        """
        return self._num_of_onlookers

    def get_length_of_generations(self) -> int:
        """
        Get the number of rounds a generation runs for in this community
        :return: The number of rounds a generation runs for
        :rtype: int
        """
        return self._length_of_generations

    def get_generations(self) -> List[Generation]:
        """
        Get a list of the generations that this community encompasses
        :return: A list of the generations that belong to this community
        :rtype: List[Generation]
        """
        return self._generations

    def get_interactions(self) -> List[Dict]:
        """
        Get the interactions that occurred through the whole community
        :return: The interactions through the whole community
        :rtype: List[Dict]
        """
        return self._interactions

    def get_interactions_by_generation(self) -> List[List[Dict]]:
        """
        Get the interactions that occurred through the whole community ordered by generation
        :return: The interactions through the whole community
        :rtype: List[Dict]
        """
        return self._interactions_by_generation

    def get_strategy_count_by_generation(self) -> List[List[Dict[str]]]:
        """
        Get the count of each strategy by generation
        :return: The strategy count for each generation
        :rtype: List[List[Dict[str]]]
        """
        return self._strategy_count_by_generation

    def get_actions(self) -> List[List[Dict]]:
        """
        Get the actions taken in this generation, indexed by timepoint
        :return: The actions in this generation, indexed by timepoint
        :rtype: Dict[int]
        """
        return self._actions

    def get_social_welfare(self) -> int:
        """
        Get the total social welfare produced by interactions in the whole community
        :return: The social welfare
        :rtype: int
        """
        return self._social_welfare

    def get_social_welfare_by_generation(self) -> List[int]:
        """
        Get the social welfare for each generation
        :return: The social welfare for each generation
        :rtype: int
        """
        return self._social_welfare_by_generation

    def get_cooperation_rate(self) -> int:
        """
        Get the rate of cooperation of the whole community
        :return: The rate of cooperation of the whole community as a percentage
        :rtype: int
        """
        return int(round(100*(self._cooperation_count/self._interaction_count)))

    def get_cooperation_rate_by_generation(self) -> List[int]:
        """
        Get the cooperation rate for each generation, the index is the generation id
        :return: The cooperation rate for each generation
        :rtype: List[int]
        """
        return self._cooperation_rate_by_generation

    def get_idleness_percentage(self) -> int:
        """
        Get the percentage of idleness of the whole community
        :return: The percentage of idleness of the whole community
        :rtype: int
        """
        return int(round(100*(self._idle_action_count/self._non_donor_action_count)))

    def get_social_activeness_percentage(self) -> int:
        """
        Get the percentage of actions where the players of the whole community were socially active
        :return: the social activeness of the players of the whole community
        :rtype: int
        """
        return int(round(100*(self._social_action_count/self._non_donor_action_count)))

    def get_fitness(self) -> int:
        """
        Get the fitness of the whole community.
        :return: The fitness of the community
        :rtype: int
        """
        return self._fitness

    def simulate(self):
        """
        Simulate the community, building an initial generation simulating that generation and then for the specified
        number of generations reproducing and simulating the next generation
        :return: void
        """
        for i in range(self._num_of_generations):
            generation = self._build_generation()
            generation.simulate()
            self._cooperation_count += generation.get_cooperation_count()
            self._interaction_count += generation.get_interaction_count()
            self._cooperation_rate_by_generation.append(generation.get_cooperation_rate())
            for timepoint in range(generation.get_start_point(), generation.get_end_point()):
                self._actions.append(generation.get_actions()[timepoint])
            self._interactions.extend(generation.get_interactions())
            self._interactions_by_generation.append(generation.get_interactions())
            self._strategy_count_by_generation.append(generation.get_strategy_count())
            self._social_welfare += generation.get_social_welfare()
            self._social_welfare_by_generation.append(generation.get_social_welfare())
            self._idle_action_count += generation.get_idle_action_count()
            self._social_action_count += generation.get_social_action_count()
            self._non_donor_action_count += generation.get_non_donor_action_count()
            self._fitness += generation.get_fitness()
            self._generations.append(generation)

    def _build_generation(self) -> Generation:
        """
        Build a generation, if is is the first generation use the initial strategies, else reproduce from the old
         generation
        :return: The next generation to simulate
        :rtype: Generation
        """
        if len(self._generations) <= 0:
            return Generation(self._first_strategies, len(self._generations), self._community_id, 0,
                              self._length_of_generations, self._num_of_onlookers, True)
        else:
            return self._reproduce()

    def _reproduce(self) -> Generation:
        """
        Use the last generation of players to build a new generation of players
        Uses the roulette wheel selection via stochastic acceptance outline by Lipowski et al. referenced in my report
        :return: The new generation
        :rtype: Generation
        """
        # Find last generation of players details
        last_gen_players = self._generations[-1].get_players()
        maximal_fitness = 0
        for player in last_gen_players:
            if player.get_fitness() > maximal_fitness:
                maximal_fitness = player.get_fitness()
        # Form new generation
        new_gen_strategies: List = []
        new_gen_size = 0
        while new_gen_size < self._generation_size:
            # Mutate to randomly selected strategy with probability selected in __init__
            if random.random() < self._mutation_chance:
                selected_strategy = random.choice(self._first_strategies)
                new_gen_strategies.append(selected_strategy['strategy'])
                new_gen_size += 1
            else:
                # If no mutation use stochastic acceptance
                selected_player = random.choice(last_gen_players)
                if random.random() <= maximal_fitness:
                    new_gen_strategies.append(selected_player.get_strategy())
                    new_gen_size += 1
        return Generation(new_gen_strategies, len(self._generations), self._community_id, self._current_time,
                          self._current_time+self._length_of_generations, self._num_of_onlookers, False)
