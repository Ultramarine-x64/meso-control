from random import random

from src.behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class MPCBehaviour(AbstractHexagonBehaviour):

    def __init__(
        self,
        agent_id: int,
        agent_location: Hexagon2DLocation,
        target_location: Hexagon2DLocation,
        walls: list,
        number_of_next_moves: int = 3
    ):
        super().__init__(agent_id, agent_location, target_location, walls)
        self.number_of_next_moves = number_of_next_moves
        self.next_moves = []
        self.messages = {}

    def compute_action(self) -> None:
        self.compute_next_move()

    def compute_next_move(self) -> None:
        if len(self.next_moves) > 0:
            return

        if self.is_random_move:
            self.next_moves.append(self.agent_location.get_random_move())
            return

        tmp_location = self.agent_location
        for _ in range(self.number_of_next_moves):
            next_move = tmp_location.compute_proportional_move(self.target_location)
            tmp_location += next_move
            self.next_moves.append(next_move)

    def correct_next_move(self) -> None:
        agent_next_locations = [
            self.messages[agent_id][0] + self.messages[agent_id][1]
            for agent_id in self.messages
            if len(self.messages[agent_id]) > 1 and agent_id < self.agent_id
        ]

        collision_with_walls = self.walls.count(self.agent_location + self.next_moves[0]) > 0
        collision_with_agents = agent_next_locations.count(self.agent_location + self.next_moves[0]) > 0
        if collision_with_walls or collision_with_agents:
            self.obstacle_avoidance()

    def do_action(self) -> None:
        if self.num_penalty_step != 0:
            self.num_penalty_step -= 1
            self.is_random_move = True
        else:
            self.move()

    def get_message(self) -> list:
        message = [self.agent_location]
        for move in self.next_moves:
            message.append(move)

        return message

    def move(self) -> None:
        next_move = self.next_moves[0]
        self.agent_location += next_move
        self.next_moves.remove(next_move)
        self.is_random_move = False

    def obstacle_avoidance(self) -> None:
        agent_next_locations = [
            self.messages[agent_id][0] + self.messages[agent_id][1]
            for agent_id in self.messages
            if len(self.messages[agent_id]) > 1 and agent_id < self.agent_id
        ]

        possible_moves = [
            move
            for move in self.agent_location.get_possible_moves()
            if self.walls.count(self.agent_location + move) == 0
                and agent_next_locations.count(self.agent_location + move) == 0
                and self.agent_location + move != self.previous_location
        ]

        next_move = self.next_moves[0] * -1
        for move in possible_moves:
            distance_after_next_move = self.target_location.get_distance(self.agent_location + next_move)
            distance_after_move = self.target_location.get_distance(self.agent_location + move)

            if distance_after_next_move > distance_after_move or \
                distance_after_next_move == distance_after_move and random() > 0.5:
                self.next_moves.pop(0)
                self.next_moves.append(move)
                next_move = move

    def define_cluster_target(self, messages) -> None:
        pass

    def define_center_cluster_location(self, messages: dict) -> None:
        pass

    def rec_messages(self, messages: dict) -> None:
        self.messages = messages

    def reset(self) -> None:
        pass

    def get_next_move(self) -> Hexagon2DLocation:
        if len(self.next_moves) > 0:
            return self.next_moves[0]

        return Hexagon2DLocation(0, 0)
