from random import random

from src.behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class MesoBehaviour(AbstractHexagonBehaviour):
    """Behavior implementing algorithm 2c(3).
    Agents determine the center and area of their cluster.
    Then calculate the optimal trajectory for all clusters without collisions.
    Then, moving the cluster center to the target for their cluster,
    they move themselves parallel to the movement of the cluster center.
    """

    def __init__(
        self,
        agent_id: int,
        agent_location: Hexagon2DLocation,
        cluster_radius: int,
        target_location: Hexagon2DLocation,
        walls: [],
    ):
        """Creating an instance of a class with agent id, location and target and cluster id.
        Now there is a cluster target task, but then we need to remove it,
        and the agents themselves must calculate it.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param cluster_radius: maximum cluster radius
        :type cluster_radius: int
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        :param walls: walls on hexagon plane
        :type walls: list
        """
        super().__init__(agent_id, agent_location, target_location, walls)
        self.cluster_radius = cluster_radius
        self.cluster_id = 0
        self.is_cluster_definition = False
        self.center_cluster_location = agent_location
        self.coefficient_trust = 1
        self.coefficient_confidence = 0

    def compute_action(self) -> None:
        if not self.is_cluster_definition:
            self.define_clusters(self.messages)

        self.compute_next_move()
        if self.walls.count(self.agent_location + self.next_move) > 0:
            self.obstacle_avoidance()

    def compute_next_move(self) -> None:
        if self.is_random_move:
            self.coefficient_trust = 0
            self.coefficient_confidence = 0
            self.next_move = self.agent_location.get_random_move()
        elif self.center_cluster_location == self.target_location:
            self.next_move = Hexagon2DLocation(0, 0)
        else:
            self.next_move = self.agent_location.compute_move(
                self.target_location - self.center_cluster_location + self.agent_location
            )

    # def correct_next_move(self) -> None:
    #     # Поправка только от ближайшего обходящего препятствие
    #     agent_behaviours = [
    #         message[0]
    #         for _, message in self.messages.items()
    #         if message[0].cluster_id == self.cluster_id and message[0].agent_id != self.agent_id
    #     ]
    #
    #     if self.coefficient_trust == 0 or len(agent_behaviours) == 0:
    #         return
    #
    #     nearest_agent_behaviour = agent_behaviours[0]
    #     for agent_behaviour in agent_behaviours:
    #         if (
    #             self.agent_location.get_distance(agent_behaviour.agent_location)
    #             < self.agent_location.get_distance(nearest_agent_behaviour.agent_location)
    #             and agent_behaviour.coefficient_confidence == 1
    #         ):
    #             nearest_agent_behaviour = agent_behaviour
    #
    #     if nearest_agent_behaviour.coefficient_confidence == 1:
    #         self.next_move = nearest_agent_behaviour.next_move
    #
    #     if self.walls.count(self.agent_location + self.next_move) > 0:
    #         self.obstacle_avoidance()

    def correct_next_move(self) -> None:
        # Берем от всех, но обратно пропорционально расстоянию между агентами
        agent_behaviours = [
            message[0]
            for _, message in self.messages.items()
            if message[0].cluster_id == self.cluster_id and message[0].agent_id != self.agent_id
        ]

        agent_next_move_in_degrees = self.agent_location.get_direction_in_degrees(
            self.agent_location.get_direction_to_neighbour_location(self.agent_location + self.next_move)
        )
        group_next_move_in_degrees = agent_next_move_in_degrees

        num_of_accepted_corrections = 0
        for agent_behaviour in agent_behaviours:
            agent_direction_in_degrees = agent_behaviour.agent_location.get_direction_in_degrees(
                agent_behaviour.agent_location.get_direction_to_neighbour_location(
                    agent_behaviour.agent_location + agent_behaviour.next_move
                )
            )

            group_next_move_in_degrees += (
                (agent_next_move_in_degrees - agent_direction_in_degrees)
                * agent_behaviour.coefficient_confidence
                * self.coefficient_trust
                / (self.agent_location.get_distance(agent_behaviour.agent_location) * 0.7) # 0.7 compute from expiremental
            )
            if agent_behaviour.coefficient_confidence != 0 and self.coefficient_trust != 0:
                num_of_accepted_corrections += 1

        group_next_move_in_degrees /= num_of_accepted_corrections + 1

        group_next_move_direction = Hexagon2DLocation.get_direction_from_degrees(group_next_move_in_degrees)
        self.next_move = self.agent_location.get_move(group_next_move_direction)

        if self.center_cluster_location == self.target_location:
            self.next_move = self.agent_location.compute_move(self.center_cluster_location)

        if self.walls.count(self.agent_location + self.next_move) > 0:
            self.obstacle_avoidance()

    # def define_clusters(self, messages: dict) -> None:
    #     # Жадный
    #     if len([message[0].cluster_id for _, message in messages.items()]) == 0:
    #         max_cluster_id = 0
    #     else:
    #         max_cluster_id = max([message[0].cluster_id for _, message in messages.items()])
    #     self.cluster_id = max_cluster_id + 1
    #     self.is_cluster_definition = True
    #
    #     agent_behaviours = [message[0] for _, message in messages.items()]
    #     cluster_member_locations = [self.agent_location]
    #     center_cluster_location = self.agent_location
    #
    #     for agent_behaviour in agent_behaviours:
    #         if not agent_behaviour.is_cluster_definition and self.is_agent_in_cluster_radius(
    #             agent_behaviour.agent_location, cluster_member_locations
    #         ):
    #             agent_behaviour.cluster_id = self.cluster_id
    #             agent_behaviour.is_cluster_definition = True
    #             cluster_member_locations.append(agent_behaviour.agent_location)
    #             center_cluster_location += agent_behaviour.agent_location
    #
    #     center_cluster_location //= len(cluster_member_locations)
    #     self.center_cluster_location = center_cluster_location
    #
    #     for agent_behaviour in agent_behaviours:
    #         if agent_behaviour.cluster_id == self.cluster_id:
    #             agent_behaviour.center_cluster_location = self.center_cluster_location

    # def define_clusters(self, messages: dict) -> None:
    #     # Остовное дерево
    #     agent_behaviours = [message[0] for _, message in messages.items()]
    #
    #     pairs_agent_behaviours = []
    #     for agent_behaviour_i in agent_behaviours:
    #         for agent_behaviour_j in agent_behaviours:
    #             pair_agents_distance = agent_behaviour_i.agent_location.get_distance(agent_behaviour_j.agent_location)
    #             if pair_agents_distance < self.cluster_radius and agent_behaviour_j != agent_behaviour_i:
    #                 pairs_agent_behaviours.append((agent_behaviour_i, agent_behaviour_j))
    #
    #     pairs_agent_behaviours.sort(key=lambda pair: pair[0].agent_location.get_distance(pair[1].agent_location))
    #
    #     spanning_tree = []
    #     clusters = {}
    #     cluster_id = 1
    #     # num_of_clusters = 2
    #     for pair in pairs_agent_behaviours:
    #         # if len(spanning_tree) > len(agent_behaviours) - 1 - num_of_clusters:
    #         #    break
    #         if not pair[0].is_cluster_definition and not pair[1].is_cluster_definition:
    #             pair[0].cluster_id = cluster_id
    #             pair[0].is_cluster_definition = True
    #             pair[1].cluster_id = cluster_id
    #             pair[1].is_cluster_definition = True
    #             clusters.update([(cluster_id, [pair[0], pair[1]])])
    #             spanning_tree.append(pair)
    #             cluster_id += 1
    #         elif not pair[0].is_cluster_definition and pair[1].is_cluster_definition:
    #             pair[0].cluster_id = pair[1].cluster_id
    #             pair[0].is_cluster_definition = True
    #             clusters.get(pair[1].cluster_id).append(pair[0])
    #             spanning_tree.append(pair)
    #         elif pair[0].is_cluster_definition and not pair[1].is_cluster_definition:
    #             pair[1].cluster_id = pair[0].cluster_id
    #             pair[1].is_cluster_definition = True
    #             clusters.get(pair[0].cluster_id).append(pair[1])
    #             spanning_tree.append(pair)
    #         elif pair[1].cluster_id != pair[0].cluster_id:
    #             ind = pair[1].cluster_id
    #             for behaviour in clusters.get(ind):
    #                 behaviour.cluster_id = pair[0].cluster_id
    #                 clusters.get(pair[0].cluster_id).append(behaviour)
    #             clusters.pop(ind)
    #             spanning_tree.append(pair)
    #
    #     new_cluster_id = 1
    #     for _, cluster in clusters.items():
    #         center_cluster_location = Hexagon2DLocation(0, 0)
    #         for behaviour in cluster:
    #             center_cluster_location += behaviour.agent_location
    #         center_cluster_location //= len(cluster)
    #         for behaviour in cluster:
    #             behaviour.center_cluster_location = center_cluster_location
    #             behaviour.cluster_id = new_cluster_id
    #         new_cluster_id += 1
    #
    #     for behaviour in agent_behaviours:
    #         if behaviour.cluster_id == 0:
    #             behaviour.cluster_id = new_cluster_id
    #             new_cluster_id += 1
    #             behaviour.is_cluster_definition = True

    def define_clusters(self, messages: dict) -> None:
        # Снизу вверх жадный
        agent_behaviours = [message[0] for _, message in messages.items()]
        agent_behaviours.sort(key=lambda behaviour: behaviour.agent_location.row)

        for agent_behaviour_i in agent_behaviours:
            if agent_behaviour_i.is_cluster_definition:
                continue
            max_cluster_id = max([message[0].cluster_id for _, message in messages.items()])
            agent_behaviour_i.is_cluster_definition = True
            agent_behaviour_i.cluster_id = max_cluster_id + 1
            for agent_behaviour_j in agent_behaviours:
                if agent_behaviour_j.is_cluster_definition:
                    continue
                pair_agents_distance = agent_behaviour_i.agent_location.get_distance(agent_behaviour_j.agent_location)
                if pair_agents_distance < self.cluster_radius and agent_behaviour_j != agent_behaviour_i:
                    agent_behaviour_j.is_cluster_definition = True
                    agent_behaviour_j.cluster_id = max_cluster_id + 1

        clusters = []
        for agent_behaviour in agent_behaviours:
            if len(clusters) < agent_behaviour.cluster_id:
                clusters.append([agent_behaviour])
            else:
                clusters[agent_behaviour.cluster_id - 1].append(agent_behaviour)

        for cluster in clusters:
            center_cluster_location = Hexagon2DLocation(0, 0)
            for behaviour in cluster:
                center_cluster_location += behaviour.agent_location
            center_cluster_location //= len(cluster)
            for behaviour in cluster:
                behaviour.center_cluster_location = center_cluster_location

    def do_action(self) -> None:
        self.coefficient_trust = 1
        self.coefficient_confidence = 0

        if not self.is_cluster_definition:
            return
        if self.num_penalty_step < 0:
            self.num_penalty_step = 0
        if self.num_penalty_step != 0:
            self.num_penalty_step -= 1
            self.is_random_move = True
            return
        else:
            self.move()
            self.is_random_move = False

    def get_message(self) -> list:
        return [self]

    def is_agent_in_cluster_radius(self, agent_location: Hexagon2DLocation, cluster_member_locations: list) -> bool:
        for location in cluster_member_locations:
            if agent_location.get_distance(location) > self.cluster_radius:
                return False
        return True

    def is_clusters_in_cluster_radius(self, cluster_i_members: list, cluster_j_members: list) -> bool:
        for member_i in cluster_i_members:
            for member_j in cluster_j_members:
                if member_i.agent_location.get_distance(member_j.agent_location) > self.cluster_radius:
                    return False
        return True

    def move(self) -> None:
        self.previous_location = self.agent_location
        self.agent_location += self.next_move

    def obstacle_avoidance(self) -> None:
        possible_moves = [
            move
            for move in self.agent_location.get_possible_moves()
            if self.walls.count(self.agent_location + move) == 0
            and self.agent_location + move != self.previous_location
        ]

        self.next_move *= -1
        for move in possible_moves:
            if self.target_location.get_distance(
                self.agent_location + self.next_move
            ) > self.target_location.get_distance(self.agent_location + move):
                self.next_move = move
            elif self.target_location.get_distance(
                self.agent_location + self.next_move
            ) == self.target_location.get_distance(self.agent_location + move):
                random_number = random()
                if random_number > 0.5:
                    self.next_move = move

        self.coefficient_trust = 0
        self.coefficient_confidence = 1

    def rec_messages(self, messages: dict) -> None:
        self.messages = messages

    def reset(self) -> None:
        self.cluster_id = 0
        self.is_cluster_definition = False
        self.center_cluster_location = self.agent_location

    def define_center_cluster_location(self, messages: dict) -> None:
        pass

    def define_cluster_target(self, messages) -> None:
        pass
