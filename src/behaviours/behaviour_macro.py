from random import random

from src.behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class MacroBehaviour(AbstractHexagonBehaviour):
    """Behavior implementing algorithm 2.
    Agents determine the center of their cluster by moving it to the target,
    move themselves parallel to the movement of the cluster center.
    """

    def __init__(
        self,
        agent_id: int,
        cluster_id: int,
        agent_location: Hexagon2DLocation,
        target_location: Hexagon2DLocation,
        walls: list,
    ):
        """Creating an instance of a class with agent id, location and target and cluster id.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        :param walls: walls on hexagon plane
        :type walls: list
        """
        super().__init__(agent_id, agent_location, target_location, walls)
        self.cluster_id = cluster_id
        self.center_cluster_location = agent_location
        self.is_synchronization = False

    def compute_action(self) -> None:
        if not self.is_synchronization:
            self.define_center_cluster_location(self.messages)

        self.compute_next_move()
        if self.walls.count(self.agent_location + self.next_move) > 0:
            self.obstacle_avoidance()

    def compute_next_move(self):
        if self.is_random_move:
            self.next_move = self.agent_location.get_random_move()
        elif self.center_cluster_location == self.target_location:
            self.next_move = Hexagon2DLocation(0, 0)
        else:
            self.next_move = self.agent_location.compute_move(
                self.target_location - self.center_cluster_location + self.agent_location
            )

    def correct_next_move(self) -> None:
        if self.center_cluster_location == self.target_location:
            self.next_move = self.agent_location.compute_move(self.center_cluster_location)

        if self.walls.count(self.next_move + self.agent_location) > 0:
            self.obstacle_avoidance()

    def define_center_cluster_location(self, messages: dict) -> None:
        if len(messages) == 0:
            return

        agent_locations = [message[0] for _, message in messages.items()]

        new_center_cluster_location = Hexagon2DLocation(0, 0)
        for location in agent_locations:
            new_center_cluster_location += location
        new_center_cluster_location //= len(agent_locations)

        self.center_cluster_location = new_center_cluster_location
        self.is_synchronization = True

    def do_action(self) -> None:
        if self.num_penalty_step < 0:
            self.num_penalty_step = 0
        elif self.num_penalty_step != 0:
            self.num_penalty_step -= 1
            self.is_random_move = True
        else:
            self.move()
            self.is_random_move = False

    def get_message(self) -> list:
        return [self.agent_location]

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

    def rec_messages(self, messages: dict) -> None:
        self.messages = messages

    def reset(self) -> None:
        self.is_synchronization = False

    def define_cluster_target(self, messages) -> None:
        pass
