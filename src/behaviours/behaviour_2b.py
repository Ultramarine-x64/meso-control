from src.behaviours.abstract_behaviour import AbstractBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class Behaviour2B(AbstractBehaviour):
    """!!!DEPRECATED!!!
    Behavior implementing cluster local tracking.
    """

    def __init__(self, agent_id: int, agent_location: Hexagon2DLocation, target_location: Hexagon2DLocation):
        """Creating an instance of a class with agent id, location and target.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        """
        super().__init__(agent_id)
        self.agent_location = agent_location
        self.target_location = target_location
        self.cluster_location = agent_location
        self.is_synchronization = False
        self.is_random_move = False

    def do_action(self) -> None:
        if self.target_location != self.cluster_location:
            if self.is_synchronization:
                self.move()
                self.num_penalty_step = 0
        else:
            if self.num_penalty_step != 0:
                self.num_penalty_step -= 1
                self.is_random_move = True
            else:
                self.move()

    def get_handling_message(self, messages: dict) -> Hexagon2DLocation:
        handling_message = Hexagon2DLocation(0, 0)
        for _, message in messages.items():
            handling_message += message
        handling_message //= len(messages)

        return handling_message

    def get_message(self) -> Hexagon2DLocation:
        return self.cluster_location

    def rec_messages(self, messages: dict) -> None:
        if not self.is_synchronization:
            self.cluster_location = self.get_handling_message(messages)
            self.update_synchronization(messages)

    def move(self) -> None:
        """Updates self.agent_location and self.cluster_location for move to target location."""
        if self.target_location != self.cluster_location:
            tmp_move = self.cluster_location.compute_move(self.target_location)
            self.agent_location += self.get_move()
            self.cluster_location += tmp_move
        else:
            self.agent_location += self.get_move()
        self.is_random_move = False

    def update_synchronization(self, messages: dict) -> None:
        for _, message in messages.items():
            if message != self.cluster_location:
                return

        self.is_synchronization = True

    def get_move(self) -> Hexagon2DLocation:
        if self.target_location != self.cluster_location:
            return self.agent_location.compute_move(self.target_location - self.cluster_location + self.agent_location)
        else:
            if self.is_random_move:
                return self.agent_location.get_random_move()
            else:
                return self.agent_location.compute_move(self.target_location)
